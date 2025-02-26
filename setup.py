import setuptools
"""
打包成一个 可执行模块
"""
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ApiRunner",
    version="0.0.1",
    author="cocozxf",
    author_email="154016994@qq.com",
    description="api 接口自动化测试工具",
    license="GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/cocozxf/apirunner03"
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pytest",
        'pytest-html',
        "jsonpath",
        "PyYAML",
        "pyyaml-include",
        "requests"
    ],
    packages=setuptools.find_packages(),

    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            # 可执行文件的名称=执行的具体代码方法
            'apirun=apirunner.cli.cli:main'
        ]
    },
    zip_safe=False
)