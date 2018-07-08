"""
    一个完整的程序
"""
from flask import Flask  # 导入Flask类
from flask import request, make_response, redirect, abort
from flask_script import Manager

app = Flask(__name__)  # 创建程序实例，Flask类的对象，有个指定的参数。程序主模块或包的名字
manager = Manager(app)

# 处理URL和函数之间关系的程序称为路由
# 定义路由的最简便方式，使用程序实例提供的app.route修饰器，把修饰的函数注册为路由


@app.route('/')  # / 表示程序的跟地址，hello_world()函数注册为程序跟地址的处理程序
def hello_world():  # 视图函数
    return 'Hello World!'  # 返回值称为响应，是客户端接收的内容
    # return redirect("http://www.baidu.com")

# 尖括号里面的内容就是动态部分，调用函数的时候，Flask会把动态部分作为参数传入函数
# 动态部分默认使用字符串，看可以指定类型。如下：


@app.route("/user/<name>/<int:num>")  # todo 动态路由
def user(name, num):
    return "<h1>Hello , %s ,  %d </h1>" % (name, num)


# todo 2.5.1 程序上下文和请求上下文
"""
    使用上下文临时把某些对象变为全局看可访问。
"""


@app.route("/browser")
def req():
    user_agent = request.headers.get("User-Agent")
    host = request.host
    return "You browser is %s ; host is : %s" % (user_agent, host)
# 在上面这个视图函数中，把request看出了全局变量使用。事实上，request不可能是全局变量。
# 试想：在多线程服务器中，多个线程同时处理不同的客户端发送过来的不同请求，每个线程看到的request对象必然不同


# todo 2.5.2 请求调度
"""
    程序收到客户端发送过来的请求时，要找到处理该请求的视图函数
    可以通过app.url_map 查看当前程序中的URL映射是什么样子，分别对应的视图函数。
    URL映射是URL和视图函数之前的对应关系
"""

# todo 2.5.3 请求钩子
"""
    请求钩子使用修饰器实现。Flask支持一下4种钩子
    before_first_request
    before_request
    after_request
    teardown_request
    
    在请求钩子函数和视图函数之前共享数据一般使用上下文全局变量g。
"""

# todo 2.5.4 响应
"""
    Http相应中有一个很重要的就是状态码。Flask默认是200。
如果视图函数返回的响应需要不同的状态码，可以把数字代码作为第二个返回值。如下：
"""


@app.route("/state")
def state_code():
    return "Bad Request", 400  # 视图函数返回一个400状态码，表示请求无效


@app.route("/resp")
def respon():  # todo 不太会，好像没怎么用过
    response = make_response("<h1>This document carries a cookie</h1>")
    response.set_cookie("answer", '32')  # 设置cookie
    return response  # 返回一个response对象


@app.route("/error")
def error():
    abort(401)  # abort函数，用于处理错误
    # abort 不会把控制权交还给调用它的视图，而是抛出异常把控制权交给Web服务器


# todo 2.6 Flask扩展


if __name__ == '__main__':  #
    # app.run(debug=True)  # 通过run()方法启动Flask，可通过设置debug参数为True开启调式模式
    manager.run()