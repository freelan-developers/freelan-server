"""
The API join network view.
"""

from freelan_server.database import Network

from flask.views import MethodView

from flask import request, jsonify
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

        super(ApiJoinNetworkView, self).__init__()

        self.app = app

    def post(self):

        network_name = request.json.get('network')

        network = Network.query.filter(Network.name == network_name).first();

        if not network or not network in current_user.networks:
            return 'No network match the specified name. ("%s")' % network_name, 403

        users_certificates = [
            user.certificate_string for user in network.users
            if (user != current_user) and user.certificate_string
        ]

        # TODO: Implement the line below
        users_endpoints = []

        # FIXME: Make the following IP addresses dynamic
        result = {
            'ipv4_address_prefix_length': '9.0.0.2/24',
            'ipv6_address_prefix_length': 'fe80::2/64',
            'users_certificates': users_certificates,
            'users_endpoints': users_endpoints,
        }

        return jsonify(result)
