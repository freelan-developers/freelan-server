"""
The API login view.
"""

import pkg_resources

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template, jsonify
from flask_login import current_user, login_user
from freelan_server.database import User
from freelan_server.forms.login import LoginForm

class ApiLoginView(MethodView):
    """
    The API login view.
    """

    def get(self):

        distribution = pkg_resources.require('freelan_server')[0]

        return jsonify(
            name=distribution.project_name,
            version=distribution.version,
        )
