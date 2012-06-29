"""
The settings view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, login_required
from freelan_server.database import DATABASE, Setting

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

        for key in self.known_keys:
            if key in request.values:
                setting = Setting.query.get(key)

                if setting:
                    setting.value = request.values[key]
                else:
                    setting = Setting(key, request.values[key])

                DATABASE.session.add(setting)
                DATABASE.session.commit()

        return self.get()
