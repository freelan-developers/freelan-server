"""
The API login view.
"""

import os
import base64

from flask.views import MethodView

from flask import url_for, request, session, jsonify
from flask_login import login_user
from freelan_server.database import User

class ApiLoginView(MethodView):
    """
    The API login view.
    """

    def get(self):

        challenge = base64.b64encode(os.urandom(32));

        session['api.challenge'] = challenge

        result = {
            'challenge': challenge,
        }

        return jsonify(**result)

    def post(self):

        if session.new:
            return "No session could be found. Have you performed a GET first ?", 403

        challenge = session.get('api.challenge')

        if not challenge:
            return "No challenge information was found. Have you performed a GET first ?", 403

        if (request.json.get('challenge') != challenge):
            return "Challenges do not match. Unable to continue.", 403

        user = User.query.filter_by(username=request.json.get('username')).first()

        if not user or not user.check_password(request.json.get('password')):
            return "Invalid username or password.", 403

        session.regenerate()

        login_user(user, remember=False)

        return jsonify()
