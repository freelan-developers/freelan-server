"""
The API join network view.
"""

from datetime import datetime, timedelta

from freelan_server.database import DATABASE, Network

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
        endpoints = request.json.get('endpoints')

        network = Network.query.filter(Network.name == network_name).first();

        if not network or not network in current_user.networks:
            return 'No network match the specified name. ("%s")' % network_name, 403

        if not endpoints:
            return 'No endpoints specified.', 403

        current_user.join_network(
            network=network,
            endpoints=endpoints,
            validity_date=datetime.now() + timedelta(seconds=self.app.config['NETWORK_MEMBERSHIP_VALIDITY_DURATION']),
        )

        DATABASE.session.commit()

        users_certificates = [
            user.certificate_string for user in network.users
            if (user != current_user) and user.certificate_string
        ]

        users_endpoints = [
            ep for ep in (
                am.endpoint for am in network.active_memberships
                if (am.user != current_user) and (am.validity_date > datetime.now())
            )
        ]

        # FIXME: Make the following IP addresses dynamic
        result = {
            'ipv4_address_prefix_length': '9.0.0.2/24',
            'ipv6_address_prefix_length': 'fe80::2/64',
            'users_certificates': users_certificates,
            'users_endpoints': users_endpoints,
        }

        return jsonify(result)
