"""
The user view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template, abort
from flask_login import current_user, login_required
from freelan_server.database import User

class UserView(MethodView):
    """
    The user view.
    """

    decorators = [login_required]

    def get(self, user_id):

        user = User.query.get(user_id)

        if not user:
            return abort(404);

        return render_template('pages/user/display.html')

    def post(self):
        return render_template('pages/user/display.html')

    def delete(self, user_id):
        return render_template('pages/user/display.html')

    def put(self, user_id):
        return render_template('pages/user/display.html')

