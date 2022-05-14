from flask import render_template, flash, redirect, url_for, request, jsonify
from app.main.auth import auth
from app.forms import RegisterForm, LoginForm, CommentForm, PitchForm
from app.main.landing import landing
from app.models import User, Pitch, Comment, Like, Dislike
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import desc
from app import photos
import os
from app.email import mail_message

# Authentication Views Start


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            user_email = User.query.filter_by(email=email).first()
            if user_email:
                flash("Email or username is already in use")
                return render_template('accounts/register.html', form=form)
            username = form.username.data
            password = form.password.data
            user = User(username=username, email=email, password=password)
            user.save()
            flash("Account created successfully")
            mail_message("Welcome to Elevator Pitches!",
                         "email/welcome_user", email, user=user)
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


@login_required
@auth.route('/logout')
def logout():
    logout_user()
    flash("Logged Out Successfully!")
    return redirect(url_for('landing.index'))


@auth.route('/forgot_password')
def forgot_password():
    return {'Email': 'brian@gmail.com'}
# Authentication Views End


# Homepage View
@landing.route('/')
def index():
    comment_form = CommentForm()
    pitches = pitch_repr(Pitch.query.all())
    latest_pitches = pitch_repr(Pitch.query.order_by(desc('created_at'))[:4])
    return render_template('index.html', pitches=pitches, latest_pitches=latest_pitches, comment_form=comment_form)


def pitch_repr(pitches):
    for pitch in pitches:
        pitch.user = User.query.filter_by(id=pitch.author_id).first()
        for comment in pitch.comments:
            comment.user = User.query.filter_by(id=comment.user_id).first()
    return pitches


# User Pitches View
@login_required
@landing.route('/<int:user_id>/pitches')
def pitches(user_id):
    comment_form = CommentForm()
    pitches = Pitch.query.filter_by(
        author_id=user_id).all()
    return render_template('pitches.html', pitches=pitches, comment_form=comment_form)


# Add New Pitch View
@login_required
@landing.route('/pitches/<int:user_id>/new', methods=['GET', 'POST'])
def new_pitch(user_id):
    form = PitchForm()
    if form.validate_on_submit():
        body = form.body.data
        category = form.category.data
        pitch = Pitch(author_id=user_id, body=body, category=category)
        pitch.save()
        return redirect(request.args.get('next') or url_for('landing.pitches', user_id=user_id))
    return render_template('forms/new_pitch.html', form=form)


# Add comment to pitch view
@login_required
@landing.route('/comment/<int:pitch_id>/add', methods=['POST'])
def add_comment(pitch_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(body=form.body.data,
                              user_id=current_user.id, pitch=pitch_id)
        new_comment.save()
        user = User.query.filter_by(id=current_user.id).first()
        comment = {'body': form.body.data,
                   'user': user.username, 'pitch': pitch_id}
        flash("Comment added successfully!")
        return jsonify(comment)
    return render_template('index.html')


# Add like to Pitch
@login_required
@landing.route('/pitch/<string:vote>/<int:pitch_id>', methods=['POST'])
def toggleVotes(vote, pitch_id):
    if vote == 'like':
        new_like = Like(user_id=current_user.id, pitch_id=pitch_id)
        new_like.toggleVote()
    elif vote == 'dislike':
        new_dislike = Dislike(user_id=current_user.id, pitch_id=pitch_id)
        new_dislike.toggleVote()
    likes = Like.query.filter_by(pitch_id=pitch_id).count()
    dislikes = Dislike.query.filter_by(pitch_id=pitch_id).count()

    return jsonify(likes, dislikes)


@landing.route('/<int:user_id>/profile', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    if 'photo' in request.files:
        if user.profile_pic_path:
            user_image = f"/{user.profile_pic_path.split('/')[1]}"
            path = os.path.abspath(os.environ.get(
                'UPLOADED_PHOTOS_DEST') + user_image)
            if os.path.exists(path):
                os.remove(path)

        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user.save()
        return redirect(url_for('landing.profile', user_id=user_id))
    return render_template('profile.html', user=user)
