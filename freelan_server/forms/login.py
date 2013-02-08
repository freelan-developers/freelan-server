"""
The login form.
"""

from flask_wtf import Form, TextField, PasswordField, RecaptchaField, BooleanField, validators

class LoginForm(Form):
    """
    The login form.
    """
    username = TextField('Username', [validators.Required(), validators.Length(min=1, max=80)])
    password = PasswordField('Password', [validators.Required()])
    recaptcha = RecaptchaField()
    remember_me = BooleanField('Remember me')
