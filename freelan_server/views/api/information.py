"""
The API information view.
"""

from freelan_server.extensions.version import NAME, VERSION

from flask.views import MethodView

from flask import session, url_for, jsonify

class ApiInformationView(MethodView):
    """
    The API information view.
    """

    def get(self):

        result = {
            'name': NAME,
            'major': VERSION.split('.')[0],
            'minor': VERSION.split('.')[1],
            'login_url': url_for('api/login'),
        }

        return jsonify(**result)
