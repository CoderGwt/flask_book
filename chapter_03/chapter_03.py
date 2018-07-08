# todo 第三章：模板
from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

# todo 3.1.1 渲染模板


@app.route('/')
def hello_world():
    # return 'Hello World!'
    return render_template("index.html", current_time=datetime.utcnow())  # 渲染模板


"""
    默认情况下，Flask在程序文件夹中的templates子文件夹中寻找模块
"""


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)


"""
    Flask提供的render_template函数把Jinja2模板引擎集成到程序中来。
    render_template第一个参数就是模板文件名（html文件），随后的参数都是键值对
    
    例中：name=name是关键字参数；
            左边的“name” 表示参数名，就是模板中要使用的占位符
            右边的“name"表示当前作用域中的变量，表示同名参i数的值      
"""

# todo 3.1.2 变量
"""
    在模板中使用{{ name }}结构表示一个变量，
        它是一种特殊的占位符，告诉模板引擎这个位置的值从渲染模板时使用的数据中获取
    Jinja能够识别所有类型的变量，包括复杂的字典，列表，对象等等

    可以使用过滤器修改变量，过滤器名添加在变量名之后，中间使用竖线分割。
"""
# 例子：模板以首字母大写形式显示变量name的值 {{ name | capitalize}}


# todo 3.1.3 控制结构
"""
    Jinja2提供了多种控制结构，可用来改变模板的渲染流程
"""


@app.route("/control/<name>")
def control(name):
    li = [i for i in range(len(name))]
    return render_template("user.html", name=name, li=li)


# todo 3.2 使用Flask-Bootstrap集成Twitter Bootstrap
"""
    Bootstrap 是客户端框架
"""

# todo 3.3 自定义错误界面
"""
    Flask允许程序使用基于模板的自定义错误页面。
    最常见的错误代码有两个：   
        404：客户端请求未知页面或路由时显示
        500：有未处理的异常时显示
"""


@app.errorhandler(404)  # 客户端请求未知页面或路由时触发该视图函数
def page_not_found(e):
    return render_template("404.html"), 404  # 返回404响应


@app.errorhandler(500)  # 有未处理的异常时触发该视图函数
def internal_server_error(e):
    return render_template("500.html"), 500  # 返回500响应


# todo 3.4 链接
"""
    url_for() 辅助函数，可以使用程序URL映射中保存的信息生成的URL
    url_for()函数最简单的用法就是使用视图函数名作为参数，返回对应的URL
"""


@app.route("/url")
def url():
    return url_for("hello_world")  # 返回视图函数对于的URL,可添加参数，返回完整的URL

# todo 3.5 静态文件


"""
    静态文件的应用被当作是一个特殊的路由 /static/<filename>
    默认设置下：Flask在程序跟目录汇总的static子目录中寻找静态文件，
      如果需要，可在static文件夹中使用子文件夹存放文件。
      服务器收到前面那个URL后，会生成一个响应，包含文件系统中static/css/style.css文件的内容
"""

# todo 使用Flask-moment本地化时间和日期
"""
    服务器需要同意时间单位，和用户所处的地理位置没有关系。
    UTC
    把时间单位交给Web浏览器，转换成当地时间，然后渲染。
    Web浏览器可以更好的完成这一任务，因为它能获取用户电脑中的时区和区域设置
    
    使用Flask-Moment扩展 
"""


@app.route("/time")
def show_time():
    return render_template("index.html", current_time=datetime.utcnow())


if __name__ == '__main__':
    app.run(debug=True)
