"""
The API login view.
"""

import pkg_resources

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template, jsonify
from flask_login import current_user, login_user
from freelan_server.database import User

class ApiLoginView(MethodView):
    """
    The API login view.
    """

    def get(self):
        pass

    def post(self):

        distribution = pkg_resources.require('freelan_server')[0]

        result = {
            'name': distribution.project_name,
            'version': distribution.version,
        }

        user = User.query.filter_by(username=request.json.get('username')).first()

        if user and user.check_password(request.json.get('password')):

            # Fix for a bug in Flask-KVSession
            if not hasattr(session, 'sid_s'):
                session.sid_s = None

            session.regenerate()
            login_user(user, remember=False)
        else:
            result['error'] = 'Invalid username or password.'

        response = jsonify(**result)
        response.status_code = ('error' in result) and 403 or 200

        return response
