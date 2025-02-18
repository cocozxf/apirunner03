# 工具封装思路
2. 框架遗留的问题： 虽然只需要填充数据，但是对测试人员还是有一定的要求 
3. 如果仅仅只是定义数据，有更友好的方式，例如：json配置文件、yaml配置文件、excel配置方式..等等
4. 更高级的工具化 -- 让使用者脱离代码 -- 构建一个命令行工具


# 工具封装一个过程
1. 梳理目标 - 【只要会运行程序，完全不写代码，只需要配置文件】
2. 梳理问题 - 
* 【框架中数据的定义方式】
  * 用到yaml文件定义框架执行所需要的数据，因为yaml和字典对象能够方便转换
* 【多组测试用例的执行方式】
  * 如果你只是一个测试用例。固定读取某一个yaml文件
  * 有多个用例的存在， 不可避免的需要编写多个 pytest测试方法
  * 有没有办法 pytest固定写一个，适应不同的用例执行？？
* 【一个pytest测试方法如何执行不同的用例】
  * 基于pytest的**参数化** 
  * 只需要在pytest执行测试方法之前，把不同的测试用例信息读取为 **pytest参数化**的数据即可 【Pytest插件】
* 【一个用例有多组数据怎么办？】
  * 此时代码里面只有一个pytest方法， 参数全部都是 ”测试用例的信息“，**不是测试用例里面的数据**
  * 测试用例配置里面，增加一个数据驱动DDT配置项
  * 加载测试用例信息的时候， 根据DDT配置项，生成不同的数据的测试用例
* 【固定的测试用例配置文件目录】
  * 通过配置项，去指定读取任意文件夹下面的 yaml文件
  * 添加一个 --cases=文件夹路径 
* 【还是需要打开项目运行python代码】
  * 有没有办法，不需要开发环境，仅需安装python运行环境即可 实现工具运行？
  * setuptools
  * `python setup.py install` 生成
  * celery -A app.my_celery worker -l INFO -P eventlet
