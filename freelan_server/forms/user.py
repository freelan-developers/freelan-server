"""
The user form.
"""

from flask_wtf import Form, TextField, FormField, FieldList, PasswordField, BooleanField, validators
from flask_wtf.html5 import EmailField
from freelan_server.extensions.fields import ConstantField, IPTextField

class UserMemberForm(Form):
    """
    The user member form.
    """
    network_id = ConstantField('Identifier')
    network_name = ConstantField('Network')
    is_member = BooleanField('Is member')
    ipv4_address = IPTextField('IPv4 address', ip_version=4, network_only=False)
    ipv6_address = IPTextField('IPv6 address', ip_version=6, network_only=False)

class UserForm(Form):
    """
    The user form.
    """
    username = TextField('Username', [validators.Required(), validators.Length(min=1, max=80)])
    current_password = PasswordField('Current password', [validators.Optional()])
    new_password = PasswordField('New password', [validators.Optional()])
    new_password_repeat = PasswordField('Repeat new password', [validators.EqualTo('new_password', message='Passwords must match.')])
    email = EmailField('Email', [validators.Required()])
    networks = FieldList(FormField(UserMemberForm))
    admin_flag = BooleanField('Has administrative privileges');
