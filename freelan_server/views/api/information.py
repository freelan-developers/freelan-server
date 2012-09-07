"""
The API information view.
"""

import pkg_resources

from flask.views import MethodView

from flask import session, jsonify

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
        }

        return jsonify(**result)
