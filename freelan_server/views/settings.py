"""
The settings view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, login_required
from freelan_server.database import Setting

class SettingsView(MethodView):
    """
    The settings view.
    """

    decorators = [login_required]

    def get(self):

        all_settings = Setting.query.all()

        known_keys = [
            'authority_certificate',
            'authority_private_key',
        ]

        settings = dict((s.key, s.value) for s in all_settings if s.key in known_keys)
        unknown_settings = dict((s.key, s.value) for s in all_settings if s.key not in known_keys)

        return render_template('pages/settings.html', unknown_settings=unknown_settings, **settings)
