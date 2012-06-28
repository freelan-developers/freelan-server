"""
The settings view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, login_required

class SettingsView(MethodView):
    """
    The settings view.
    """

    decorators = [login_required]

    def get(self):

        return render_template('pages/settings.html')
