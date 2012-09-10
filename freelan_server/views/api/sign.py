"""
The API sign view.
"""

import base64

from flask.views import MethodView

from flask import request, session, jsonify
from flask_login import current_user, login_required

class ApiSignView(MethodView):
    """
    The API sign view.
    """

    decorators = [login_required]

    def post(self):

        certificate_request = base64.b64decode(request.json.get('certificate_request'));

        #TODO: Implement

        return jsonify()
