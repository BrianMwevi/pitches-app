from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, EmailField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email
from app.models import User


class RegisterForm(FlaskForm):

    email = EmailField('Email', validators=[Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("That username is taken")
