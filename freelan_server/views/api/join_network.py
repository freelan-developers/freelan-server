"""
The API join network view.
"""

from datetime import datetime

from freelan_server.database import DATABASE, Network, UserInNetwork

from flask.views import MethodView

from flask import request, jsonify
from flask_login import current_user, login_required

import IPy

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

        def replace_host_part(endpoint):
            try:
                index = endpoint.rindex(':')
                host_part = endpoint[:index]
                port_part = endpoint[index + 1:]

                if host_part.startswith('[') and host_part.endswith(']'):
                    host_part = host_part[1:-1]

                ip_address = IPy.IP(host_part)

                if not ip_address.ip:
                    new_host_part = request.host[:request.host.rindex(':')]

                    if ':' in new_host_part:
                        return '[%s]:%s' % (new_host_part, port_part)
                    else:
                        return '%s:%s' % (new_host_part, port_part)

            except ValueError:
                pass

            return endpoint

        endpoints = list(set(map(replace_host_part, endpoints)))

        current_user.join_network(
            network=network,
            endpoints=endpoints,
        )

        DATABASE.session.commit()

        users_certificates = [
            user.certificate_string for user in network.users
            if (user != current_user) and user.certificate_string
        ]

        # FIXME: Doesn't work as intended: always returns an empty list
        memberships = [membership for membership in network.memberships if membership.user != current_user]
        all_endpoints = [endpoint for endpoint in membership.raw_endpoints for membership in memberships]
        valid_endpoints = [endpoint for endpoint in all_endpoints if (datetime.now() - endpoint.creation_date) <= self.app.config['NETWORK_MEMBERSHIP_VALIDITY_DURATION']]

        # FIXME: Make the following IP addresses dynamic
        result = {
            'ipv4_address_prefix_length': '9.0.0.2/24',
            'ipv6_address_prefix_length': 'fe80::2/64',
            'users_certificates': users_certificates,
            'users_endpoints': valid_endpoints,
        }

        return jsonify(result)
