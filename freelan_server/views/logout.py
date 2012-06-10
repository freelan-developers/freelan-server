"""
The logout view.
"""

from flask.views import MethodView

from flask import redirect, url_for, flash
from flask_login import current_user, logout_user

class LogoutView(MethodView):
    """
    The logout view.
    """

    def get(self):
        if current_user.is_authenticated():
            flash('You are not longer logged in.', 'info')

        logout_user()

        return redirect(url_for('root'))
