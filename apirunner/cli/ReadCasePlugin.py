import copy
import os

import pytest
import yaml
from yamlinclude import YamlIncludeConstructor

from apirunner.cli.DataCenter import DataCenter


class ReadCasePlugin:
    """
    pytest插件 - 用于pytest运行时的用例配置信息加载
    """

    def pytest_addoption(self, parser):
        """
        增加pytest运行的配置项
        """
        parser.addoption(
            "--cases", action="store", default="../examples", help="测试用例目录"
        )

    def yaml_include(loader, node):
        """
        加载yaml文件中引用的其他yaml文件
        """
        # 获取这个yaml文件的路径
        file_name = os.path.join(os.path.dirname(loader.name), node.value)

        with open(file_name) as yamlfile:
            return yaml.load(yamlfile)

    def pytest_collectstart(collector):
        protected_dirs = [
            "C:\\Documents and Settings",
            "C:\\System Volume Information",
            "C:\\ProgramData"
        ]
        if hasattr(collector, "path"):
            for protected_dir in protected_dirs:
                if str(collector.path).startswith(protected_dir):
                    pytest.skip(f"Skipping protected directory: {collector.path}")

    def pytest_collection_modifyitems(self, items):
        for item in items:
            item.name = item.name.encode("utf-8").decode("unicode_escape")
            item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

    def pytest_configure(self, config):
        """
        pytest配置过程中，把用例数据读取到DataCenter对象里面去
        """
        # 配置pytest
        config_path = os.path.abspath(config.getoption("--cases"))

        print("pytest用例读取中...", config_path)
        DataCenter.caseinfos = []
        DataCenter.ids = []
        YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader)

        # 读取指定文件夹下的yaml文件
        for yfile in os.listdir(config_path):
            # 如果不是以test开头，yaml文件后缀，则不处理该文件
            if not yfile.startswith("test") or not yfile.endswith("yaml"):
                continue

            # 每个文件里面描述一个业务场景 - 一个场景可能由多组数据测试组成多个测试用例
            rfile = open(os.path.join(config_path, yfile), "r", encoding='utf-8')
            caseinfo = yaml.full_load(rfile)
            rfile.close()
            # 读取DDT节点 --- 生成多组测试用例，交个pytest去执行
            ddts = caseinfo.get("ddts", [])
            if len(ddts) > 0:
                caseinfo.pop("ddts")

            if len(ddts) == 0:
                DataCenter.caseinfos.append(caseinfo)
                taskname = caseinfo.get("desc", "").encode("utf-8").decode("utf-8")
                DataCenter.ids.append(taskname)
            else:
                # 循环生成多个用例执行对象，保存起来。
                for ddt in ddts:
                    new_case = copy.deepcopy(caseinfo)
                    # 将数据读取后更新到 context 里面
                    context = new_case.get("context", {})
                    ddt.update(context)
                    new_case.update({"context": ddt})
                    DataCenter.caseinfos.append(new_case)
                    DataCenter.ids.append(ddt["desc"])

        print(DataCenter.caseinfos)
