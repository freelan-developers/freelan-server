"""
The freelan-server entry point.
"""

from flask import Flask

APPLICATION = Flask(__name__)

APPLICATION.config.from_object('freelan_server.default_configuration')
APPLICATION.config.from_envvar('FREELAN_SERVER_CONFIGURATION_FILE', silent=True)

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
