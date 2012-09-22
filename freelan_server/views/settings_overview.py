"""
The settings overview view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, login_required

import M2Crypto as m2

class SettingsOverviewView(MethodView):
    """
    The settings overview view.
    """

    decorators = [login_required]

    def __init__(self, app):
        """
        Initialize the view.

        app is the application.
        """

        self.app = app

    def get(self):
        """
        Get the settings page.
        """

        return render_template(
            'pages/settings_overview.html',
            authority_certificate_file=self.app.config['AUTHORITY_CERTIFICATE_FILE'],
            authority_certificate=self.app.config['AUTHORITY_CERTIFICATE'],
            authority_certificate_error=self.app.config['AUTHORITY_CERTIFICATE_ERROR'],
            authority_private_key_file=self.app.config['AUTHORITY_PRIVATE_KEY_FILE'],
            authority_private_key=self.app.config['AUTHORITY_PRIVATE_KEY'],
            authority_private_key_error=self.app.config['AUTHORITY_PRIVATE_KEY_ERROR'],
        )
