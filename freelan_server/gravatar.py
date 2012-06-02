"""
Gravatar related classes and functions.
"""

from freelan_server import APPLICATION

from flaskext.gravatar import Gravatar

GRAVATAR = Gravatar(
    app=APPLICATION,
    size=128,
    rating='pg',
    default='identicon',
)

