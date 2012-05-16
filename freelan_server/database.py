"""
Database models.
"""

from freelan_server import APPLICATION

from flask.ext.sqlalchemy import SQLAlchemy

from flaskext.login import UserMixin

import datetime

DATABASE = SQLAlchemy(APPLICATION)

class User(DATABASE.Model, UserMixin):
    """
    Represents a database user.
    """

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    username = DATABASE.Column(DATABASE.String(80), unique=True, nullable=False)
    email = DATABASE.Column(DATABASE.String(254), unique=True)
    password_hash = DATABASE.Column(DATABASE.String(50))
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False)

    def __init__(self, username, email, password):
        """
        Initializes a new user.
        """

        self.username = username
        self.email = email
        self.password = password
        self.creation_date = datetime.datetime.now()

    def __repr__(self):
        """
        Gives a representation of the user.
        """

        return '<User %r>' % self.username

    def check_password(self, password):
        """
        Check if the specified password matches the one of the user.

        Return True if the password matches, False otherwise.
        """

        from werkzeug import check_password_hash

        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        """
        Sets the user password.

        The specified password is salted and hashed and can thus *NEVER* be recovered.
        """

        from werkzeug import generate_password_hash

        self.password_hash = generate_password_hash(password)

    password = property(fset=set_password)
