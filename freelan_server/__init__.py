"""
The freelan-server entry point.
"""

from flask import Flask
from simplekv.memory import DictStore
from flaskext.kvsession import KVSessionExtension

APPLICATION = Flask(__name__)

APPLICATION.config.from_object('freelan_server.default_configuration')
APPLICATION.config.from_envvar('FREELAN_SERVER_CONFIGURATION_FILE', silent=True)

# We make the version information available to the templates
from freelan_server.version import VERSION

@APPLICATION.context_processor
def add_version():
    """
    Make the version information available to the templates.
    """

    return {'version': VERSION}

# We replace the default session mechanism
STORE = DictStore()
KVSessionExtension(STORE, APPLICATION)

# We import the views
# This must be done **AFTER** the APPLICATION object is instanciated.
from freelan_server.views import *
