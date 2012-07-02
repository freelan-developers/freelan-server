"""
X509 certificate related functions.
"""

def register_certificate_functions(app):
    """
    Register certificate related methods to the specified Flask application.
    """

    def empty(s):
        """
        Decorate the specified string with the empty markers and returns it.
        """

        return '<em class="empty">%s</em>' % s

    @app.template_filter()
    def x509_name(name):
        """
        Outputs the X509 name.
        """

        if name:

            result = '''
            <dl>
                <dt>Country</dt>
                <dd>%(country)s</dd>
                <dt>State</dt>
                <dd>%(state)s</dd>
                <dt>Organisational Unit</dt>
                <dd>%(organisational_unit)s</dd>
                <dt>Common name</dt>
                <dd>%(common_name)s</dd>
                <dt>Email</dt>
                <dd>%(email)s</dd>
            </dl>
            ''' % {
                'country': name.C or empty('Country'),
                'state': name.ST or empty('No state'),
                'organisational_unit': name.OU or empty('No organisational unit'),
                'common_name': name.CN or empty('No common name'),
                'email': name.Email or empty('No email')
            }

        else:
            result = empty('No name')

        return result

    @app.template_filter()
    def x509_certificate(cert):
        """
        Outputs the X509 certificate.
        """

        if cert:

            extensions = [cert.get_ext(i) for i in xrange(cert.get_ext_count())]

            result = '''
            <dl class="certificate">
                <dt>Subject</dt>
                <dd>%(subject)s</dd>
                <dt>Issuer</dt>
                <dd>%(issuer)s</dd>
                <dt>Version</dt>
                <dd>%(version)s</dd>
                <dt>Serial number</dt>
                <dd>%(serial_number)s</dd>
                <dt>Not before</dt>
                <dd>%(not_before)s</dd>
                <dt>Not after</dt>
                <dd>%(not_after)s</dd>
                <dt>Fingerprint</dt>
                <dd>%(fingerprint)s</dd>
                <dt>Extensions</dt>
                <dd>%(extensions)s</dd>
            </dl>
            ''' % {
                'subject': x509_name(cert.get_subject()),
                'issuer': x509_name(cert.get_issuer()),
                'version': cert.get_version(),
                'serial_number': cert.get_serial_number(),
                'not_before': cert.get_not_before(),
                'not_after': cert.get_not_after(),
                'fingerprint': cert.get_fingerprint(),
                'extensions': extensions or empty('No extensions'),
            }

        else:
            result = empty('No certificate')

        return result
