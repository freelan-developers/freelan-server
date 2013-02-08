"""
The register form.
"""

from flask_wtf import Form, TextField, PasswordField, RecaptchaField, validators, ValidationError
from flask_wtf.html5 import EmailField
from freelan_server.database import User

def username_check(form, field):
    if field.data:
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('A user with that username already exists.')

def email_check(form, field):
    if field.data:
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('A user with that email address already exists.')

class RegisterForm(Form):
    """
    The register form.
    """
    username = TextField('Username', [validators.Required(), validators.Length(min=1, max=80), username_check])
    password = PasswordField('Password', [validators.Required()])
    password_repeat = PasswordField('Repeat password', [validators.EqualTo('password', message='Passwords must match.')])
    email = EmailField('Email', [validators.Required(), email_check])
    recaptcha = RecaptchaField()
