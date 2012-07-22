"""
The users view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, login_required

from freelan_server.database import User

from sqlalchemy import desc

class UsersView(MethodView):
    """
    The users view.
    """

    decorators = [login_required]

    def get(self):

        users = User.query.order_by(desc(User.admin_flag)).order_by(User.username).all()

        return render_template('pages/users.html', users=users)
