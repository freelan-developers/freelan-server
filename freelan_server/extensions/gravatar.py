"""
Gravatar related classes and functions.
"""

from flaskext.gravatar import Gravatar

def register_gravatar_information(app):
    """
    Register gravatar-related methods to the specified Flask application.
    """

    gravatar = Gravatar(
        app=app,
        size=128,
        rating='pg',
        default='identicon',
    )
