"""
The login form.
"""

from wtforms import TextField, PasswordField, RecaptchaField, BooleanField
from flask_wtf import Form, validators

class LoginForm(Form):
    """
    The login form.
    """
    username = TextField('Username', [validators.Required(), validators.Length(min=1, max=80)])
    password = PasswordField('Password', [validators.Required()])
    recaptcha = RecaptchaField()
    remember_me = BooleanField('Remember me')
