"""
Gravatar related classes and functions.
"""

from flaskext.gravatar import Gravatar

def register_gravatar_filters(app):
    """
    Register gravatar-related filters to the specified Flask application.
    """

    gravatar = Gravatar(
        app=app,
        size=128,
        rating='pg',
        default='identicon',
    )
