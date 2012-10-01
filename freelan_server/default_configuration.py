"""
The default configuration.
"""

import os
import tempfile

# The host to listen on.
HOST = '::'

# Whether to enable debug mode.
DEBUG = False

# The authority certificate file.
#
# An absolute path to the authority certificate file.
AUTHORITY_CERTIFICATE_FILE = ''

# The authority private key file.
#
# An absolute path to the authority private key file.
AUTHORITY_PRIVATE_KEY_FILE = ''

# The authority private key passphrase.
#
# If no passphrase is required, specify None.
AUTHORITY_PRIVATE_KEY_PASSPHRASE = None

# The issued certificate validity duration, in days.
CERTIFICATE_VALIDITY_DURATION = 3

# The database URI.
#
# For real installations, you probably want to change the target directory to a
# more permanent location or to change the database provider to something more
# production-suited.
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(
    tempfile.gettempdir(),
    'freelan_server.db'
)

# The secret key used for session securing.
#
# This key *MUST* be changed and kept secret !
#
# Failing to do so would allow anyone to steal sessions and you don't want
# that, do you ?
SECRET_KEY = 'please change this secret key'
