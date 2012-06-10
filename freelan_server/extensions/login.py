"""
Login related classes and functions.
"""

from flask_login import LoginManager, login_url
from flask import redirect, request, flash
from freelan_server.database import User

def register_login_information(app):
    """
    Register login-related methods to the specified Flask application.
    """

    login_manager = LoginManager()
    login_manager.setup_app(app)

    @login_manager.user_loader
    def load_user(userid):
        """
        Load a user from its identifier.

        Return None if no such user is found.
        """

        return User.query.get(int(userid))

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Please log in to access this page.', 'error')

        return redirect(login_url('login', request.url))
