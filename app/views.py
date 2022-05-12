from flask import render_template, flash, redirect, url_for, request
from app.main.auth import auth
from app.forms import RegisterForm, LoginForm, CommentForm, PitchForm
from app.main.landing import landing
from app.models import User, Pitch, Comment
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import desc


# Authentication Views Start
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User(username=username, email=email, password=password)
        user.save()
        flash("Account created successfully")
        return redirect(url_for('auth.login'))
    return render_template('accounts/register.html', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            login_user(user, form.remember_me)
            flash("Logged In Successfully!")
            return redirect(request.args.get('next') or url_for('landing.pitches', user_id=user.id))
        flash('Invalid email or password')
    return render_template('accounts/login.html', form=form)

