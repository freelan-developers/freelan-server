"""
The default configuration.
"""

import os
import tempfile

HOST = '::'
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(
    tempfile.gettempdir(),
    'freelan_server.db'
)

