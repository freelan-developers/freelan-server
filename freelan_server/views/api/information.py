"""
The API information view.
"""

import pkg_resources

from flask.views import MethodView

from flask import session, url_for, jsonify

class ApiInformationView(MethodView):
    """
    The API information view.
    """

    def get(self):

        distribution = pkg_resources.require('freelan_server')[0]

        result = {
            'name': distribution.project_name,
            'major': distribution.version.split('.')[0],
            'minor': distribution.version.split('.')[1],
            'login_url': url_for('api/login'),
        }

        return jsonify(**result)
