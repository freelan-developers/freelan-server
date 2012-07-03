"""
The settings wizard view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, login_required
from freelan_server.database import DATABASE, Setting

import M2Crypto as m2

class SettingsWizardView(MethodView):
    """
    The settings wizardview.
    """

    decorators = [login_required]

    def get(self):
        """
        Get the settings wizard page.
        """

        return render_template(
            'pages/settings_wizard.html',
        )

    post = get
