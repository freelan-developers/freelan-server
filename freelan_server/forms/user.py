"""
The user form.
"""

from flask_wtf import Form, TextField, PasswordField, BooleanField, validators
from flask_wtf.html5 import EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from freelan_server.database import Network
from freelan_server.extensions.widgets import Select

class UserForm(Form):
    """
    The user form.
    """
    username = TextField('Username', [validators.Required(), validators.Length(min=1, max=80)])
    current_password = PasswordField('Current password', [validators.Optional()])
    new_password = PasswordField('New password', [validators.Optional()])
    new_password_repeat = PasswordField('Repeat new password', [validators.EqualTo('new_password', message='Passwords must match.')])
    email = EmailField('Email', [validators.Required()])
    networks = QuerySelectMultipleField(query_factory=lambda: Network.query.all(), allow_blank=True, widget=Select(multiple=True, labelizer=lambda network: network.name))
