"""
X509 crypto related functions.
"""

import binascii

def register_crypto_functions(app):
    """
    Register crypto related methods to the specified Flask application.
    """

    def empty(s):
        """
        Decorate the specified string with the empty markers and returns it.
        """

        return '<em class="empty">%s</em>' % s

    def informative(s):
        """
        Decorate the specified string with the informative markers and returns it.
        """

        return '<em class="informative">%s</em>' % s

    @app.template_filter()
    def x509_extensions(exts):
        """
        Outputs the X509 extensions.
        """

        if exts:
            result = '<dl class="x509-extension">'

            for ext in exts:
                result = result + '<dt>%(name)s%(critical)s</em></dt><dd>%(value)s</dd>' % {
                    'name': ext.get_name(),
                    'value': ext.get_value(),
                    'critical': ext.get_critical() and informative(' (critical)') or '',
                }

            result = result + '</dl>'
        else:
            result = empty('No extensions')

        return result

    @app.template_filter()
    def x509_name(name):
        """
        Outputs the X509 name.
        """

        if name:

            result = '''
            <dl class="x509-name">
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

            extensions = [cert.get_ext_at(i) for i in xrange(cert.get_ext_count())]

            result = '''
            <dl class="x509-certificate">
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
                'extensions': x509_extensions(extensions),
            }

        else:
            result = empty('No certificate')

        return result

    @app.template_filter()
    def rsa_key(key):
        """
        Outputs the RSA key.
        """

        if key:

            def split_line(line):
                """
                Split the given line into several, smaller lines of the same size.
                """

                import re

                return re.sub(r'(.{32})', lambda g: '%s<br />' % g.group(0), line)

            exponent, modulus = key.pub()

            result = '''
            <dl class="rsa-key">
                <dt>Exponent</dt>
                <dd>%(exponent)s</dd>
                <dt>Modulus size</dt>
                <dd>%(modulus_size)s</dd>
                <dt>Modulus</dt>
                <dd>%(modulus)s</dd>
            </dl>
            ''' % {
                'exponent': int(binascii.hexlify(exponent), 16),
                'modulus_size': len(modulus),
                'modulus': split_line(modulus.encode('hex').upper()),
            }

        else:
            result = empty('No rsa key')

        return result
