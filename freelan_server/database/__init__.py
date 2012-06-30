"""
Database models.
"""

from freelan_server import APPLICATION

from flask.ext.sqlalchemy import SQLAlchemy

from flask_login import UserMixin

import datetime

DATABASE = SQLAlchemy(APPLICATION)

class Setting(DATABASE.Model):
    """
    Represents a setting.
    """

    key = DATABASE.Column(DATABASE.String(64), primary_key=True)
    value = DATABASE.Column(DATABASE.Text())
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False)

    def __init__(self, key, value=None):
        """
        Initializes a new setting.
        """

        self.key = key
        self.value = value
        self.creation_date = datetime.datetime.now()

    @staticmethod
    def get(key):
        """
        Get a setting with the specified key or create one if none exists.
        """

        setting = Setting.query.get(key)

        if not setting:
            setting = Setting(key)

        return setting

    @staticmethod
    def get_value(key, default=None):
        """
        Get a setting's value.
        """

        setting = Setting.query.get(key)

        if not setting:
            return default

        return setting.value

    @staticmethod
    def set_value(key, value):
        """
        Set a setting.

        The setting change is added to the current database session, but it is still up to you to commit that session.
        """

        setting = Setting.get(key)
        setting.value = value
        DATABASE.session.add(setting)

NetworkUserTable = DATABASE.Table(
    'network_user',
    DATABASE.Column('network_id', DATABASE.Integer, DATABASE.ForeignKey('network.id')),
    DATABASE.Column('user_id', DATABASE.Integer, DATABASE.ForeignKey('user.id')),
)

class User(DATABASE.Model, UserMixin):
    """
    Represents a database user.
    """

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    username = DATABASE.Column(DATABASE.String(80), unique=True, nullable=False)
    email = DATABASE.Column(DATABASE.String(254), unique=True)
    password_hash = DATABASE.Column(DATABASE.String(50), nullable=False)
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False)
    admin_flag = DATABASE.Column(DATABASE.Boolean(), nullable=False)

    def __init__(self, username, email, password, admin_flag=False):
        """
        Initializes a new user.
        """

        self.username = username
        self.email = email
        self.password = password
        self.creation_date = datetime.datetime.now()
        self.admin_flag = admin_flag

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

class Network(DATABASE.Model):
    """
    Represents a database network.
    """

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    name = DATABASE.Column(DATABASE.String(80), unique=True, nullable=False)
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False)
    users = DATABASE.relationship('User', secondary=NetworkUserTable, backref='networks')

    def __init__(self, name):
        """
        Initialize a new network.
        """

        self.name = name
        self.creation_date = datetime.datetime.now()
