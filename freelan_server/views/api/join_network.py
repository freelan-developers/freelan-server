"""
The API join network view.
"""

import base64
from datetime import datetime, timedelta

from freelan_server.database import Network

from M2Crypto import RSA, X509, EVP, ASN1

from flask.views import MethodView

from flask import request, session, jsonify
from flask_login import current_user, login_required

class ApiJoinNetworkView(MethodView):
    """
    The API join network view.
    """

    decorators = [login_required]

    def __init__(self, app):
        """
        Initialize the view.

        app is the application.
        """

        self.app = app

    def post(self):

        if not self.app.config['AUTHORITY_CERTIFICATE']:
            return 'The server lacks an authority certificate. Unable to sign the certificate request.', 403

        network_name = request.json.get['network']

        network = Network.query.filter(Network.name == network_name).first();

        if not network or not network in current_user.networks:
            return 'No network match the specified name. ("%s")' % network_name, 403

        result = {
            'authority_certificate': base64.b64encode(self.app.config['AUTHORITY_CERTIFICATE'].as_der()),
        }

        return jsonify(result)
