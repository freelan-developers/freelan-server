"""
The freelan-server entry point.
"""

# Create the application object
from flask import Flask

APPLICATION = Flask(__name__)

APPLICATION.config.from_object('freelan_server.default_configuration')
APPLICATION.config.from_envvar('FREELAN_SERVER_CONFIGURATION_FILE', silent=True)

# Replace the default session mechanism
from simplekv.memory import DictStore
from flaskext.kvsession import KVSessionExtension

STORE = DictStore()
KVSessionExtension(STORE, APPLICATION)

# Register all extensions
from freelan_server.extensions import register_all_extensions
register_all_extensions(APPLICATION)

# Import the views
from freelan_server.views import setup_views
setup_views(APPLICATION)
