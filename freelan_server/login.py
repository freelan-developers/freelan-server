"""
Login related classes and functions.
"""

from freelan_server import APPLICATION

from flaskext.login import LoginManager
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

LOGIN_MANAGER.login_view = 'login'
LOGIN_MANAGER.login_message = 'Please log in to access this page.'
