from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import required


class NameForm(FlaskForm):
    """
        todo form 表单类
    """
    name = StringField("What's you name ? ", validators=[required()])
    submit = SubmitField("Submit")
