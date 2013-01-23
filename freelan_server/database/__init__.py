"""
Database models.
"""

import base64

from freelan_server import APPLICATION

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

from flask_login import UserMixin

import datetime

import M2Crypto as m2

DATABASE = SQLAlchemy(APPLICATION)

class UserInNetwork(DATABASE.Model):
    """
    Represents a user within a network.
    """

    network_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('network.id'), primary_key=True)
    user_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('user.id'), primary_key=True)
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False)
    ipv4_address = DATABASE.Column(DATABASE.String(64), unique=False, nullable=True)
    ipv6_address = DATABASE.Column(DATABASE.String(64), unique=False, nullable=True)
    raw_endpoints = DATABASE.relationship('Endpoint', backref='user_in_network', primaryjoin='(Endpoint.user_in_network_network_id == UserInNetwork.network_id) & (Endpoint.user_in_network_user_id == UserInNetwork.user_id)')
    endpoints = association_proxy('raw_endpoints', 'value')

    def __init__(self, network=None, user=None):
        """
        Initializes a new user-in-network.
        """

        self.creation_date = datetime.datetime.now()
        self.network = network
        self.user = user

class Endpoint(DATABASE.Model):
    """
    Represents an endpoint.
    """

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    user_in_network_network_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('user_in_network.network_id'))
    user_in_network_user_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('user_in_network.user_id'))
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False)
    value = DATABASE.Column(DATABASE.String(64), unique=False, nullable=False)
    __table_args__ = (DATABASE.UniqueConstraint('user_in_network_network_id', 'user_in_network_user_id', 'value', name='endpoint_uc'),)

    def __init__(self, value):
        """
        Initializes a new user-in-network.
        """

        self.creation_date = datetime.datetime.now()
        self.value = value

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
    memberships = DATABASE.relationship('UserInNetwork', backref='user')
    networks = association_proxy('memberships', 'network', creator=lambda network: UserInNetwork(network=network))

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

    def get_membership(self, network):
        """
        Get the network membership.
        """

        return UserInNetwork.query.filter_by(user=self, network=network).first()

    def set_endpoints(self, network, endpoints):
        """
        Set the endpoints.
        """

        membership = self.get_membership(network)

        if not membership:
            raise ValueError('Unable to set endpoints for a network the user doesn\'t belong to.')

        membership.endpoints = endpoints or []

    password = property(fset=set_password)
    certificate = property(fget=get_certificate, fset=set_certificate)

class Network(DATABASE.Model):
    """
    Represents a database network.
    """

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    name = DATABASE.Column(DATABASE.String(80), unique=True, nullable=False)
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False)
    ipv4_address = DATABASE.Column(DATABASE.String(64), unique=False, nullable=True)
    ipv6_address = DATABASE.Column(DATABASE.String(64), unique=False, nullable=True)
    memberships = DATABASE.relationship('UserInNetwork', backref='network')
    users = association_proxy('memberships', 'user', creator=lambda user: UserInNetwork(user=user))

    def __init__(self, name=''):
        """
        Initialize a new network.
        """

        self.name = name
        self.creation_date = datetime.datetime.now()
        self.ipv4_address = None
        self.ipv6_address = None
