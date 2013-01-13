"""
Database models.
"""

import base64

from freelan_server import APPLICATION

from flask.ext.sqlalchemy import SQLAlchemy

from flask_login import UserMixin

import datetime

import M2Crypto as m2

DATABASE = SQLAlchemy(APPLICATION)

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
    certificate_string = DATABASE.Column(DATABASE.String(), nullable=True)
    active_memberships = DATABASE.relationship('ActiveMembership', backref='user')

    def __init__(self, username='', email=None, password='', admin_flag=False, certificate=None):
        """
        Initializes a new user.
        """

        self.username = username
        self.email = email
        self.password = password
        self.creation_date = datetime.datetime.now()
        self.admin_flag = admin_flag
        self.certificate_string = None

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

    def get_certificate(self):
        """
        Get the last generated certificate.
        """

        if self.certificate_string:

            try:
                return m2.X509.load_cert_string(
                    base64.b64decode(self.certificate_string),
                    m2.X509.FORMAT_DER
                )

            except:
                self.certificate_string = None

    def set_certificate(self, certificate):
        """
        Set the last generated certificate.
        """

        if certificate:
            self.certificate_string = base64.b64encode(certificate.as_der())

        else:
            self.certificate_string = None

    def join_network(self, network, endpoints):
        """
        Join a network.
        """

        if not self in network.users:
            raise ValueError('Unable to join a network the user doesn\'t belong to.')

        existing_endpoints = dict((x.endpoint, x) for x in self.active_memberships)

        for endpoint in endpoints:
            if endpoint in existing_endpoints:
                existing_endpoints[endpoint].creation_date = datetime.datetime.now()
            else:
                self.active_memberships.append(
                    ActiveMembership(
                        user=self,
                        network=network,
                        endpoint=endpoint,
                    )
                )

    def leave_network(self, network):
        """
        Leave a network.
        """

        if not self in network.users:
            raise ValueError('Unable to leave a network the user doesn\'t belong to.')

        self.active_memberships = [x for x in self.active_memberships if x.network != network]

    def get_active_memberships(self, network):
        """
        Get the user active memberships on the specified network if any, or an
        empty list otherwise.
        """

        if not self in network.users:
            raise ValueError('Unable to check active membership to a network the user doesn\'t belong to.')

        return [x for x in self.active_memberships if x.network == network]

    password = property(fset=set_password)
    certificate = property(fget=get_certificate, fset=set_certificate)

class Network(DATABASE.Model):
    """
    Represents a database network.
    """

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    name = DATABASE.Column(DATABASE.String(80), unique=True, nullable=False)
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False)
    users = DATABASE.relationship('User', secondary=NetworkUserTable, backref='networks')
    ipv4_address = DATABASE.Column(DATABASE.String(64), unique=False, nullable=True)
    ipv6_address = DATABASE.Column(DATABASE.String(64), unique=False, nullable=True)
    active_memberships = DATABASE.relationship('ActiveMembership', backref='network')

    def __init__(self, name=''):
        """
        Initialize a new network.
        """

        self.name = name
        self.creation_date = datetime.datetime.now()
        self.ipv4_address = None
        self.ipv6_address = None

class ActiveMembership(DATABASE.Model):
    """
    Represents the active membership of a user to a network.
    """

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    user_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('user.id'))
    network_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('network.id'))
    endpoint = DATABASE.Column(DATABASE.String(64), unique=False, nullable=False)
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False)

    def __init__(self, user, network, endpoint):
        """
        Initialize a new active membership.
        """

        self.user = user
        self.network = network
        self.endpoint = endpoint
        self.creation_date = datetime.datetime.now()
