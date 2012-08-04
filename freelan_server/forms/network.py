"""
The network form.
"""

from flask_wtf import Form, TextField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from freelan_server.database import User
from freelan_server.extensions.widgets import Select
from freelan_server.extensions.fields import IPTextField

class NetworkForm(Form):
    """
    The network form.
    """
    name = TextField('Name', [validators.Required(), validators.Length(min=1, max=80)])
    users = QuerySelectMultipleField('Users', query_factory=lambda: User.query.all(), allow_blank=True, widget=Select(multiple=True, labelizer=lambda user: user.username))
    ipv4_address = IPTextField('IPv4 network', ip_version=4, network_only=True)
    ipv6_address = IPTextField('IPv6 network', ip_version=6, network_only=True)
