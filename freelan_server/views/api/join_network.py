"""
The API join network view.
"""

from freelan_server.database import DATABASE, Network, Endpoint

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

        Endpoint.remove_out_of_date(validity_duration=self.app.config['NETWORK_MEMBERSHIP_VALIDITY_DURATION'])

        network_name = request.json.get('network')
        endpoints = request.json.get('endpoints')

        network = Network.query.filter(Network.name == network_name).first();

        if not network or not current_user in network:
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
                    new_host_part = request.remote_addr

                    if ':' in new_host_part:
                        return '[%s]:%s' % (new_host_part, port_part)
                    else:
                        return '%s:%s' % (new_host_part, port_part)

            except ValueError:
                pass

            return endpoint

        endpoints = map(lambda e: Endpoint(value=e), set(map(replace_host_part, endpoints)))

        current_user.set_endpoints(
            network=network,
            endpoints=endpoints,
        )

        DATABASE.session.commit()

        users_certificates = [
            membership.user.certificate_string for membership in network.memberships
            if (membership.user != current_user) and membership.user.certificate_string
        ]

        users_endpoints = [
            endpoint.value for endpoint in network.get_endpoints(validity_duration=self.app.config['NETWORK_MEMBERSHIP_VALIDITY_DURATION'], exclude_users=[current_user])
        ]

        result = {
            'ipv4_address_prefix_length': network.get_ipv4_address_prefix_length(current_user),
            'ipv6_address_prefix_length': network.get_ipv6_address_prefix_length(current_user),
            'users_certificates': users_certificates,
            'users_endpoints': users_endpoints,
        }

        return jsonify(result)
