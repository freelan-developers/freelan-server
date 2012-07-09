"""
The settings wizard view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template, abort
from flask_login import current_user, login_required
from freelan_server.database import DATABASE, Setting

import M2Crypto as m2

class SettingsWizardView(MethodView):
    """
    The settings wizard view.
    """

    decorators = [login_required]

    def get(self):
        """
        Get the settings page.
        """

        authority_certificate = Setting.get_value('authority_certificate')
        authority_private_key = Setting.get_value('authority_private_key')

        return render_template(
            'pages/settings_wizard.html',
            authority_certificate=authority_certificate,
            authority_private_key=authority_private_key,
        )

    def post(self):
        """
        Update the settings.
        """

        # TODO: Handle the request

        pass
