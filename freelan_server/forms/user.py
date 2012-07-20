"""
The user form.
"""

from flask_wtf import Form, TextField, PasswordField, BooleanField, validators
from flask_wtf.html5 import EmailField

class UserForm(Form):
    """
    The user form.
    """
    username = TextField('Username', [validators.Required(), validators.Length(min=1, max=80)])
    current_password = PasswordField('Current password', [validators.Optional()])
    new_password = PasswordField('New password', [validators.Optional()])
    new_password_repeat = PasswordField('Repeat new password', [validators.EqualTo('new_password', message='Passwords must match.')])
    email = EmailField('Email', [validators.Required()])
