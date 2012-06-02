"""
Login related classes and functions.
"""

from freelan_server import APPLICATION

from flask import redirect, request, flash
from flask_login import LoginManager, login_url
from freelan_server.database import User

LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.setup_app(APPLICATION)

@LOGIN_MANAGER.user_loader
def load_user(userid):
    """
    Load a user from its identifier.

    Return None if no such user is found.
    """

    return User.query.get(int(userid))

@LOGIN_MANAGER.unauthorized_handler
def unauthorized():
    flash('Please log in to access this page.', 'error')

    return redirect(login_url('login', request.url))
