"""
The settings overview view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, login_required
from freelan_server.database import DATABASE, Setting

import M2Crypto as m2

class SettingsOverviewView(MethodView):
    """
    The settings overview view.
    """

    decorators = [login_required]

    def get(self):
        """
        Get the settings page.
        """

        try:
            authority_certificate = m2.X509.load_cert_string(
                str(Setting.get_value('authority_certificate', default='')),
                m2.X509.FORMAT_PEM
            )
        except m2.X509.X509Error, ex:
            authority_certificate = None

        try:
            authority_private_key = m2.RSA.load_key_string(str(Setting.get_value('authority_private_key', default='')), callback=(lambda v: ''))
            Setting.set_value('authority_private_key', authority_private_key)
        except m2.RSA.RSAError, ex:
            authority_private_key = None

        if authority_certificate and authority_private_key:
            evp_pkey = m2.EVP.PKey()
            evp_pkey.assign_rsa(authority_private_key)

            certificate_verify_success = authority_certificate.verify(evp_pkey)

        return render_template(
            'pages/settings_overview.html',
            authority_certificate=authority_certificate,
            authority_private_key=authority_private_key,
            certificate_verify_success=certificate_verify_success,
        )
