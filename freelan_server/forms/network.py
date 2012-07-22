"""
The network form.
"""

from flask_wtf import Form, TextField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from freelan_server.database import User
from freelan_server.extensions.widgets import Select

class NetworkForm(Form):
    """
    The network form.
    """
    name = TextField('Name', [validators.Required(), validators.Length(min=1, max=80)])
    users = QuerySelectMultipleField(query_factory=lambda: User.query.all(), allow_blank=True, widget=Select(multiple=True, labelizer=lambda user: user.username))
