from flask import Flask, render_template, url_for, session, redirect, flash
from flask_wtf import Form, FlaskForm  # Form好像是被弃用了
from wtforms.validators import required, Required
from wtforms import StringField, SubmitField  # 导入相应的字段
from wtforms.validators import Email,Length, NumberRange
from wtforms import PasswordField, TextAreaField,DateField,DateTimeField
from flask_bootstrap import Bootstrap

'''
    1.FlaskForm 和 Form的区别
    2.required 和 Required 的区别？后者好像被弃用了
'''

app = Flask(__name__)
boostrap = Bootstrap(app)

"""
    默认情况下，Flask-WTF能保护所有表单免受跨站请求伪造的攻击
    恶意网站把请求发送到被攻击者已登录的其他网站时就会引起CSRF攻击
    
    为了实现CSRF保护，Flask-WTF需要程序设置一个密钥
    Flask-WTF使用这个密钥生成加密令牌，再用令牌验证请求中表达数据的真伪
"""

# todo 4.1 跨站请求伪造保护 CSRF攻击

app.config['SECRET_key'] = "this is the secret "  # 设置密钥
app.secret_key = "why why and why "
# app.config字典可用来储存框架，扩展和程序本身的配置变量

# todo 4.2 表单类


class NameForm(FlaskForm):  # 每一个表单类都必须基础自Form类
    # 可选参数 validators 指定了一个有验证函数组成的列表
    name = StringField("What is you name ? ", validators=[required()])
    submit = SubmitField("Submit")

# todo 在视图函数中处理表单


# @app.route('/', methods=['GET', "POST"])
# 添加methods参数告诉Flask在URL映射中把这个视图函数注册为GET和POST请求的处理程序
# 如果没有methods参数，默认把视图函数注册为GET请求的处理程序
# 把POST加入方法列表很有必要，因为将表单提交作为POST请求进行处理更加便利
# def index():
#     name = None  # 用来保存存放在表单中输入的有效名字，初始化为None
#     form = NameForm()  # 创建一个NameForm类实例用于表示表单。
#     if form.validate_on_submit():
#         """
#             提交表单后，如果数据能被所有验证函数接受，那么validate_on_submit()返回True
#             否则就返回False。【第一次打开页面的时候，就是False】
#         """
#         name = form.name.data  # 用户输入的信息可以通过字段的data属性获取
#         form.name.data = ""  # 清空表单字段内容。
#     return render_template('index.html', form=form, name=name)

'''
    以上这个视图函数存在一个可用性的问题；当用户输入名字提交后，然后点击刷新，会看到一个莫名其妙的提示，需要点击确认
    出现的原因是：刷新页面时浏览器会 重新 发送之前已经发送过的最后一个请求。
    如果请求是一个包含表单数据的POST请求，刷新页面之后会再次提交表单，这并不是理想的处理方式。
    所以，有了以下的改进方法。
    使用重定向，别让Web程序把POST请求作为浏览器发送的最后一个请求
    
'''

# todo 重定向（redirect） 和  用户会话（session）
"""
    重定向redirect
    用户会话session，储存用户的信息
"""


@app.route("/", methods=['POST', 'GET'])
def index():
    form = NameForm()
    if form.validate_on_submit():

        old_name = session.get("name")  # 获取保存到session中的名字

        if old_name is not None and old_name != form.name.data:  # 判断新的名字和原来的是否一样
            flash("Looks like you have changed you name!")  # flash提示消息

        session['name'] = form.name.data  # 把输入的名字保存到session会话中

        return redirect(url_for("index"))  # redirect的参数是重定向的URL。
        # 推荐使用url_for()生成URl，因为这个函数通过URL映射生成URl，从而保证URL和定义的路由兼容，而且，修改路由名字后依然可用
    return render_template('index.html', form=form, name=session.get("name"))  # 渲染模板


"""
    以上的一个视图函数，使用重定向作为POST请求的响应，而不是使用常规响应。
    重定向是一种特殊的响应，响应内容是URL，而不是包含HTML代码的字符串
    浏览器看到这种响应时，会向重定向的URL发起get请求，显示页面内容。
    
    这种技巧成为 Post/重定向/Get模式
    
    但是会带来一个问题。程序处理POST请求时，使用form.name.data获取用户输入的名字时，可是一旦这个请求结束，数据也就丢失了
    
    因为这个POST请求使用重定向处理，所以需要程序需要保存输入的名字，这样重定向后的请求才能获得并使用这个名字，从而构建真正的响应
    
    程序可以把数据储存在用户会话中，在请求之间 ‘记住’ 数据。
    用户会话是一种私有存储，存在与每个连接到服务端的客户端中。是请求上下文的变量，名为session，像标准的Python字典一样操作
    
    存储数据：session['变量名'] = 值
    获取数据：session.get('变量名')
    
"""


if __name__ == '__main__':
    app.run(debug=True)
