"""
The settings view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, login_required
from freelan_server.database import DATABASE, Setting

import M2Crypto as m2

class SettingsView(MethodView):
    """
    The settings view.
    """

    decorators = [login_required]

    def get(self):
        """
        Get the settings page.
        """

        authority_certificate = Setting.get_value('authority_certificate')
        authority_private_key = Setting.get_value('authority_private_key')

        return render_template(
            'pages/settings.html',
            authority_certificate=authority_certificate,
            authority_private_key=authority_private_key,
        )

    def post(self):
        """
        Update the settings.
        """

        authority_certificate_error = None
        authority_certificate = request.values['authority_certificate']
        authority_private_key_error = None
        authority_private_key = request.values['authority_private_key']

        if authority_certificate:
            try:
                cert = m2.X509.load_cert_string(str(authority_certificate), m2.X509.FORMAT_PEM)
                Setting.set_value('authority_certificate', authority_certificate)
            except m2.X509.X509Error, ex:
                authority_certificate_error = 'Invalid certificate: %s' % ex

        if authority_private_key:
            try:
                cert = m2.RSA.load_key_string(str(authority_private_key))
                Setting.set_value('authority_private_key', authority_private_key)
            except m2.RSA.RSAError, ex:
                authority_private_key_error = 'Invalid private key: %s' % ex

        DATABASE.session.commit()

        return render_template(
            'pages/settings.html',
            authority_certificate_error=authority_certificate_error,
            authority_certificate=authority_certificate,
            authority_private_key_error=authority_private_key_error,
            authority_private_key=authority_private_key,
        )
