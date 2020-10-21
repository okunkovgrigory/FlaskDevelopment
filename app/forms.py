from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired('Это поле является обязательным')])
    password = PasswordField(label='Password', validators=[DataRequired('Это поле является обязательным')])
    remember_me = BooleanField(label='Remember Me')
    sign_in = SubmitField(label='Sign In')


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired('Это поле является обязательным')])
    email = StringField(label='Email', validators=[DataRequired('Это поле является обязательным'), Email()])
    password = PasswordField(label='Password', validators=[DataRequired('Это поле является обязательным')])
    password_2 = PasswordField(label='Repeat password',
                               validators=[DataRequired('Это поле является обязательным'), EqualTo('password')])
    submit = SubmitField(label='Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        print(user)
        if user is not None:
            raise ValidationError('Please use a different email address.')


class MessagesForm(FlaskForm):
    messages = StringField(label='Messages', validators=[DataRequired('Это поле не должно быть пустым')])
    tag = StringField(label='Tag', validators=[DataRequired('Это поле не должно быть пустым')])
    submit = SubmitField(label='Submit')


class EditProfileForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired('Это поле не должно быть пустым')])
    about_me = TextAreaField(label='About Me', validators=[Length(max=140)])
    submit = SubmitField(label='Submit')