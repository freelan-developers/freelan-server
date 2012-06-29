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

    def __init__(self):

        self.known_keys = [
            'authority_certificate',
            'authority_private_key',
        ]

    def get(self):

        all_settings = Setting.query.all()

        settings = dict((s.key, s.value) for s in all_settings if s.key in self.known_keys)
        unknown_settings = dict((s.key, s.value) for s in all_settings if s.key not in self.known_keys)

        return render_template('pages/settings.html', unknown_settings=unknown_settings, **settings)

    def post(self):

        authority_certificate_error = None
        authority_certificate = request.values['authority_certificate']

        if authority_certificate:
            try:
                cert = m2.X509.load_cert_string(authority_certificate, m2.X509.FORMAT_PEM)
            except m2.X509.X509Error, ex:
                authority_certificate_error = 'Invalid certificate: %s' % ex


        all_settings = Setting.query.all()

        settings = dict((s.key, s.value) for s in all_settings if s.key in self.known_keys)
        unknown_settings = dict((s.key, s.value) for s in all_settings if s.key not in self.known_keys)

        return render_template(
            'pages/settings.html',
            unknown_settings=unknown_settings,
            authority_certificate_error=authority_certificate_error,
            **settings
        )
