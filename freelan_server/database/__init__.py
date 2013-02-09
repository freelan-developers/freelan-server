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

class Member(object):
    """
    A dummy class that has all the fields your heart desires.
    """
    def __init__(self, **kw):
        for attribute, value in kw.items():
            setattr(self, attribute, value)

class UserInNetwork(DATABASE.Model):
    """
    Represents a user within a network.
    """

    network_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('network.id'), primary_key=True)
    user_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('user.id'), primary_key=True)
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
    ipv4_address = DATABASE.Column(DATABASE.String(64), unique=False, nullable=True)
    ipv6_address = DATABASE.Column(DATABASE.String(64), unique=False, nullable=True)
    endpoints = DATABASE.relationship('Endpoint', backref='user_in_network', primaryjoin='(Endpoint.user_in_network_network_id == UserInNetwork.network_id) & (Endpoint.user_in_network_user_id == UserInNetwork.user_id)', cascade='all,delete,delete-orphan')
    __table_args__ = (DATABASE.UniqueConstraint('network_id', 'user_id', name='user_in_network_uc'),)

class Endpoint(DATABASE.Model):
    """
    Represents an endpoint.
    """

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    user_in_network_network_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('user_in_network.network_id'))
    user_in_network_user_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey('user_in_network.user_id'))
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
    value = DATABASE.Column(DATABASE.String(64), unique=False, nullable=False)
    __table_args__ = (DATABASE.UniqueConstraint('user_in_network_network_id', 'user_in_network_user_id', 'value', name='endpoint_uc'),)

class User(DATABASE.Model, UserMixin):
    """
    Represents a database user.
    """

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    username = DATABASE.Column(DATABASE.String(80), unique=True, nullable=False)
    email = DATABASE.Column(DATABASE.String(254), unique=True)
    password_hash = DATABASE.Column(DATABASE.String(50), nullable=False)
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
    admin_flag = DATABASE.Column(DATABASE.Boolean(), nullable=False, default=False)
    certificate_string = DATABASE.Column(DATABASE.String(), nullable=True)
    memberships = DATABASE.relationship('UserInNetwork', backref=DATABASE.backref('user', uselist=False), cascade='all,delete,delete-orphan')

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

    certificate = property(fget=get_certificate, fset=set_certificate)

    def get_membership(self, network):
        """
        Get the network membership.
        """

        return UserInNetwork.query.filter_by(user=self, network=network).first()

    def get_endpoints(self, network):
        """
        Get the endpoints associated to the specified network.
        """

        membership = self.get_membership(network)

        if not membership:
            raise ValueError('Unable to get endpoints for a network the user doesn\'t belong to.')

        return membership.endpoints

    def set_endpoints(self, network, endpoints):
        """
        Set the endpoints associated to the specified network.
        """

        membership = self.get_membership(network)

        if not membership:
            raise ValueError('Unable to set endpoints for a network the user doesn\'t belong to.')

        membership.endpoints = endpoints or []

    def get_networks(self):
        """
        Get the user networks.
        """

        def network_to_member(network):

            is_member = False
            ipv4_address = None
            ipv6_address = None

            for membership in self.memberships:
                if membership.network_id == network.id:
                    is_member = True
                    ipv4_address = membership.ipv4_address
                    ipv6_address = membership.ipv6_address

                    break

            return Member(
                network_id=network.id,
                network_name=network.name,
                is_member=is_member,
                ipv4_address=ipv4_address,
                ipv6_address=ipv6_address,
            )

        return map(network_to_member, Network.query.all())

    def set_networks(self, networks):
        """
        Set the user networks.
        """

        network_list = [x.network_id for x in networks if x.is_member]
        self.memberships = [m for m in self.memberships if m.network_id in network_list]

        for network in networks:
            if network.is_member:
                membership = next((m for m in self.memberships if m.network_id == network.network_id), None)

                if membership:
                    membership.ipv4_address = network.ipv4_address
                    membership.ipv6_address = network.ipv6_address
                else:
                    self.memberships.append(
                        UserInNetwork(
                            network_id=network.network_id,
                            user_id=self.id,
                            ipv4_address=network.ipv4_address,
                            ipv6_address=network.ipv6_address,
                        )
                    )

    networks = property(get_networks, set_networks)

class Network(DATABASE.Model):
    """
    Represents a database network.
    """

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    name = DATABASE.Column(DATABASE.String(80), unique=True, nullable=False)
    creation_date = DATABASE.Column(DATABASE.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
    ipv4_address = DATABASE.Column(DATABASE.String(64), unique=False, nullable=True)
    ipv6_address = DATABASE.Column(DATABASE.String(64), unique=False, nullable=True)
    memberships = DATABASE.relationship('UserInNetwork', backref=DATABASE.backref('network', uselist=False), cascade='all,delete,delete-orphan')

    def __contains__(self, user):
        """
        Check if a user belongs to the network.
        """

        return UserInNetwork.query.filter_by(network=self, user=user).first()

    def get_members(self):
        """
        Get the network members.
        """

        def user_to_member(user):

            is_member = False
            ipv4_address = None
            ipv6_address = None

            for membership in self.memberships:
                if membership.user_id == user.id:
                    is_member = True
                    ipv4_address = membership.ipv4_address
                    ipv6_address = membership.ipv6_address

                    break

            return Member(
                user_id=user.id,
                username=user.username,
                email=user.email,
                is_member=is_member,
                ipv4_address=ipv4_address,
                ipv6_address=ipv6_address,
            )

        return map(user_to_member, User.query.all())

    def set_members(self, members):
        """
        Set the network members.
        """

        member_list = [x.user_id for x in members if x.is_member]
        self.memberships = [m for m in self.memberships if m.user_id in member_list]

        for member in members:
            if member.is_member:
                membership = next((m for m in self.memberships if m.user_id == member.user_id), None)

                if membership:
                    membership.ipv4_address = member.ipv4_address
                    membership.ipv6_address = member.ipv6_address
                else:
                    self.memberships.append(
                        UserInNetwork(
                            network_id=self.id,
                            user_id=member.user_id,
                            ipv4_address=member.ipv4_address,
                            ipv6_address=member.ipv6_address,
                        )
                    )

    members = property(get_members, set_members)

    def get_endpoints(self, validity_duration=None):
        """
        Get the endpoints.
        """

        endpoints = []

        now = datetime.datetime.now()

        for membership in self.memberships:
            for endpoint in membership.endpoints:
                if validity_duration is None or (now - endpoint.creation_date) <= validity_duration:
                    endpoints.append(endpoint)

        return endpoints
