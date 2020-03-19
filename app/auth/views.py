from flask import render_template

from app.auth import bp
from app.auth.forms import LoginForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    return render_template('auth/login.html', title='Login', form=form)
