"""
The API get_authority_certificate view.
"""

import base64

from flask.views import MethodView

from flask import jsonify
from flask_login import login_required

class ApiGetAuthorityCertificateView(MethodView):
    """
    The API get_authority_certificate view.
    """

    decorators = [login_required]

    def __init__(self, app):
        """
        Initialize the view.

        app is the application.
        """

        self.app = app

    def get(self):

        if not self.app.config['AUTHORITY_CERTIFICATE']:
            return 'The server lacks an authority certificate. Unable to sign the certificate request.', 403

        result = {
            'authority_certificate': base64.b64encode(self.app.config['AUTHORITY_CERTIFICATE'].as_der()),
        }

        return jsonify(**result)

