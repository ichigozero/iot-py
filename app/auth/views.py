from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user
from werkzeug.urls import url_parse

from app.auth import bp
from app.auth.forms import LoginForm
from app.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'invalid')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth.login')

        return redirect(next_page)

    return render_template('auth/login.html', title='Login', form=form)
