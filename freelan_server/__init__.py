"""
The freelan-server entry point.
"""

from flask import Flask
from simplekv.memory import DictStore
from flaskext.kvsession import KVSessionExtension

APPLICATION = Flask(__name__)

APPLICATION.config.from_object('freelan_server.default_configuration')
APPLICATION.config.from_envvar('FREELAN_SERVER_CONFIGURATION_FILE', silent=True)

# We replace the default session mechanism
STORE = DictStore()
KVSessionExtension(STORE, APPLICATION)

from freelan_server.views import *

# Run the web server
def run():
    """
    Run the web server.
    """

    APPLICATION.run(
        debug=APPLICATION.config['DEBUG'],
        host=APPLICATION.config['HOST']
    )
