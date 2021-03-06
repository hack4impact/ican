from flask import flash, render_template, redirect, url_for, \
    current_app
from ..models import User
from .forms import LoginForm
from . import main
from flask.ext.login import login_user, logout_user, login_required


@main.route('/')
@main.route('/index')
def index():
    return render_template('main/landing.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    app = current_app._get_current_object()
    form = LoginForm(CSRF_ENABLED=app.config['WTF_CSRF_ENABLED'])
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            if user.is_role("admin"):
                return redirect(url_for('admin.index'))
            elif user.is_role("student"):
                return redirect(url_for('students.index'))
            else:
                return redirect(url_for('mentors.index'))
        flash('Invalid username or password.')
    return render_template('main/login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('.index'))

