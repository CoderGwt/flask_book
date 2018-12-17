from datetime import datetime
from flask import render_template, url_for, session, redirect, flash, current_app

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email


@main.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            flash("Pleased to meet you !")

            if current_app.config['FLASKY_ASMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)

        else:
            flash("Nice to meet you again !")

        session['name'] = form.name.data
        form.name.data = ""
        return redirect(url_for(".index"))
    return render_template("index.html", form=form, name=session.get("name"),
                           current_time=datetime.utcnow())
