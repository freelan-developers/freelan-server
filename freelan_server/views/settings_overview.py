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

        authority_certificate_file = self.app.config['AUTHORITY_CERTIFICATE_FILE']
        authority_private_key_file = self.app.config['AUTHORITY_PRIVATE_KEY_FILE']
        authority_private_key_passphrase = self.app.config['AUTHORITY_PRIVATE_KEY_PASSPHRASE'] or ''

        try:
            authority_certificate = m2.X509.load_cert_string(
                open(authority_certificate_file, 'r').read(),
                m2.X509.FORMAT_PEM
            )
            authority_certificate_error = None

        except (IOError, m2.X509.X509Error) as ex:
            authority_certificate = None
            authority_certificate_error = str(ex)

        try:
            authority_private_key = m2.RSA.load_key_string(
                open(authority_private_key_file, 'r').read(),
                callback=(lambda v: authority_private_key_passphrase or '')
            )
            authority_private_key_error = None

        except (IOError, m2.RSA.RSAError) as ex:
            authority_private_key = None
            authority_private_key_error = str(ex)

        return render_template(
            'pages/settings_overview.html',
            authority_certificate_file=authority_certificate_file,
            authority_certificate=authority_certificate,
            authority_certificate_error=authority_certificate_error,
            authority_private_key_file=authority_private_key_file,
            authority_private_key=authority_private_key,
            authority_private_key_error=authority_private_key_error,
        )
