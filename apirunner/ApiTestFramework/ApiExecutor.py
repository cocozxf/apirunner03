import operator
from string import Template

import requests, jsonpath, re, json, yaml


def execute(caseinfo):
    """
        http接口调用-核心执行器
    """
    steps = caseinfo["steps"]
    context = caseinfo["context"]

    for step in steps:
        # 1. 针对step字典的每个参数，进行变量渲染
        for key in step.keys():
            if not key.startswith("_"):
                # 取值渲染
                target = step.get(key)
                string = MyTemplate(json.dumps(target))
                value = string.substitute(**context)
                obj = json.loads(value)
                # 赋值
                step.update({key: obj})

        print("请求信息: ", step)
        tmpjson = None
        if type(step.get("json", None)) == str:
            tmpjson = json.loads(step.get("json", None))
        if type(step.get("json", None)) == dict:
            tmpjson = step.get("json", None)

        # 2. 具体发起请求进行操作 ，发起HTTP请求，进行返回结果断言
        response = requests.request(url=step.get("url", None),
                                    method=step.get("method", None),
                                    params=step.get("params", None),
                                    data=step.get("data", None),
                                    json=tmpjson,
                                    headers=step.get("headers", None),
                                    cookies=context.get(f"{step.get('cookie_name')}", None),
                                    timeout=step.get("timeout", None))

        if step.get("api_type") == "login":
            context.update({
                step.get("cookie_name"): response.cookies
            })

        print("响应内容: ", response.text)
        a = response.json()
        b = step.get("assert_options", [])
        # 3. 断言 怎么做?
        # 获取 target
        # value
        # type
        for assert_option in b:
            # 3.1 获取实际值
            value = None
            assert_value_tmp = assert_option["value"]
            assert_value = assert_value_tmp.replace(" ", "")
            if assert_value.startswith("$."):
                # print("aaaaa")
                value = jsonpath.jsonpath(a, assert_value)
            # else:
            #     pattern = re.compile(assert_option["value"])
            #     value = re.findall(pattern, response.text)[0]

            # 3.2 进行判断
            if assert_option["type"] == "exists":  # 存在
                assertResult = value != False
            elif assert_option["type"] == 'contains':  # 包含
                assertResult = value[0].__contains__(
                    assert_option["target"])
            elif assert_option["type"] == 'equals':  # 相同
                assertResult = str(value[0]) == assert_option["target"]
            elif assert_option["type"] == '等于':  # 数字相同
                assertResult = value[0] == int(assert_option["target"])
            # else:
            #     assertResult = getattr(operator, assert_option["type"])(
            #         float(value[0]), float(assert_option["target"]))

            assert assertResult, "断言不通过：" + assert_option["errorMsg"]

        # 4. 抽取需要传递给下一个接口的数据
        # 需要知道，抽取的数据是谁? - 支持正则表达式 和 jsonpath
        # target 抽取对象
        # varname 变量名称
        for extract_option in step.get("extract_options", []):
            # 4.1 获取目标值
            target_value = None
            if extract_option["target"].startswith("$."):
                target_value = jsonpath.jsonpath(response.json(), extract_option["target"])
            else:
                pattern = re.compile(extract_option["target"])
                target_value = re.findall(pattern, response.text)[0]
            # 4.2 更新上下文变量数据
            context.update({
                extract_option["varname"]: target_value[0]
            })

        print("上下文：", context)


class MyTemplate(Template):
    delimiter = "!"


# 写个单元测试
def test_1():
    rfile = open("../../examples/testLogin.yaml", "r", encoding='utf-8')
    caseinfo = yaml.safe_load(rfile)
    execute(caseinfo)


if __name__ == '__main__':
    test_1()
