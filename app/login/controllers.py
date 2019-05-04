from app.login.forms import LoginForm
from app.login.models import User
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

loginbp = Blueprint('login', __name__, template_folder='templates')

@loginbp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        next_page = request.args.get('next')

        user = User(form.username.data)
        if user.username and user.check_password(form.password.data):
            login_user(user)

            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index.home')

        else:
            flash('Incorrect username/password.')
            next_page = request.referrer

        return redirect(next_page)

    return render_template('login.html', form=form)


@loginbp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))