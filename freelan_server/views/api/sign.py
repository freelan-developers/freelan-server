"""
The API sign view.
"""

import base64
from datetime import datetime, timedelta

from freelan_server.database import DATABASE

from M2Crypto import RSA, X509, EVP, ASN1

from flask.views import MethodView

from flask import request, session, jsonify
from flask_login import current_user, login_required

class ApiSignView(MethodView):
    """
    The API sign view.
    """

    decorators = [login_required]

    def __init__(self, app):
        """
        Initialize the view.

        app is the application.
        """

        self.app = app

    def post(self):

        if not self.app.config['AUTHORITY_CERTIFICATE']:
            return 'The server lacks an authority certificate. Unable to sign the certificate request.', 403

        if not self.app.config['AUTHORITY_PRIVATE_KEY']:
            return 'The server lacks a private key. Unable to sign the certificate request.', 403

        certificate_request_der = base64.b64decode(request.json.get('certificate_request'));

        certificate_request = X509.load_request_der_string(certificate_request_der);

        if not (certificate_request.get_subject().CN == current_user.username):
            return 'I will not a sign certificate request for a different user ! (Got "%s" while "%s" was expected)' % (certificate_request.get_subject().CN, current_user.username), 403

        # Create a new certificate
        certificate = X509.X509()

        # Set the certificate version
        certificate.set_version(2)

        # Copy the certificate public key from the certificate request
        certificate.set_pubkey(certificate_request.get_pubkey())

        # Set the certificate issuer
        certificate.set_issuer(self.app.config['AUTHORITY_CERTIFICATE'].get_subject())

        # Set the certificate subject
        subject_name = X509.X509_Name()
        subject_name.CN = certificate_request.get_subject().CN or ''
        subject_name.OU = self.app.config['AUTHORITY_CERTIFICATE'].get_subject().OU or ''
        subject_name.O = self.app.config['AUTHORITY_CERTIFICATE'].get_subject().O or ''
        subject_name.L = self.app.config['AUTHORITY_CERTIFICATE'].get_subject().L or ''
        subject_name.ST = self.app.config['AUTHORITY_CERTIFICATE'].get_subject().ST or ''
        subject_name.C = self.app.config['AUTHORITY_CERTIFICATE'].get_subject().C or ''

        certificate.set_subject(subject_name)

        # Set the certificate "not before" timestamp
        not_before = ASN1.ASN1_UTCTIME()
        not_before.set_datetime(datetime.today() + timedelta(days=-1))

        certificate.set_not_before(not_before)

        # Set the certificate "not after" timestamp
        not_after = ASN1.ASN1_UTCTIME()
        not_after.set_datetime(datetime.today() + self.app.config['CERTIFICATE_VALIDITY_DURATION'])

        certificate.set_not_after(not_after)

        # The issued certificate shall not be used as a certificate authority
        certificate.add_ext(X509.new_extension('basicConstraints', 'CA:FALSE'))

        # Sign the certificate
        pkey = EVP.PKey()
        pkey.assign_rsa(self.app.config['AUTHORITY_PRIVATE_KEY'], capture=False)

        certificate.sign(pkey, 'sha1')

        current_user.certificate = certificate

        DATABASE.session.commit()

        result = {
            'certificate': current_user.certificate_string,
        }

        return jsonify(result)
