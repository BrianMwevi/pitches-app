from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login_manager


class CrudOperation:

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True


class User(UserMixin, db.Model, CrudOperation):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    pitches = db.relationship('Pitch', backref='pitches', lazy=True)
    profile_pic_path = db.Column(db.String, nullable=True, unique=True)

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def add_comment(self, comment):
        self.comments.append(comment)
        return self.save()

    def add_pitch(self, pitch):
        self.pitches.append(pitch)
        return self.save()

    def __repr__(self) -> str:
        return self.username


class Pitch(db.Model, CrudOperation):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    category = db.Column(db.String, default='General')
    comments = db.relationship('Comment', backref='comments', lazy=True)
    likes = db.relationship('Like', backref='likes', lazy=True)
    dislikes = db.relationship('Dislike', backref='dislikes', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def delete(self):
        user = User.query.filter_by(id=self.author).first()
        user.pitches.remove(self)
        self.delete()
        return self.save()

    def update(self):
        pitch = Pitch.query.filter_by(id=self.id).first()
        pitch.category = self.category
        pitch.body = self.body
        return pitch.save()

    def __repr__(self):
        return self.body


class Comment(db.Model, CrudOperation):
    id = db.Column(db.Integer, primary_key=True)
    pitch = db.Column(db.Integer, db.ForeignKey('pitch.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def delete(self):
        pitch = Pitch.query.filter_by(id=self.pitch).first()
        pitch.comments.remove(self)
        self.delete()
        return self.save()

    def update(self):
        comment = Comment.query.filter_by(id=self.id).first()
        comment.body = self.body
        return comment.save()

    def __repr__(self):
        return self.body


class Like(db.Model, CrudOperation):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_at = db.Column(db.DateTime, default=datetime.now())
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitch.id'))

    def toggleVote(self):
        like = Like.query.filter_by(
            pitch_id=self.pitch_id, user_id=self.user_id).first()
        dislike = Dislike.query.filter_by(
            pitch_id=self.pitch_id, user_id=self.user_id).first()
        if like is None:
            self.save()
        elif like:
            like.delete()

        if dislike:
            dislike.delete()
        return True


class Dislike(db.Model, CrudOperation):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    disliked_at = db.Column(db.DateTime, default=datetime.now())
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitch.id'))

    def toggleVote(self):
        dislike = Dislike.query.filter_by(
            pitch_id=self.pitch_id, user_id=self.user_id).first()
        like = Like.query.filter_by(
            pitch_id=self.pitch_id, user_id=self.user_id).first()

        if dislike is None:
            self.save()
        elif dislike:
            dislike.delete()
        if like:
            like.delete()
        return True
