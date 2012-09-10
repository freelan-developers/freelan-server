"""
The version information.
"""

import pkg_resources

def get_distribution():
    """
    Get the distribution.
    """

    requires = pkg_resources.require('freelan_server')

    if requires:
        return requires[0]

def get_name():
    """
    Get the current server name.
    """

    distribution = get_distribution()

    if distribution:
        return distribution.project_name

def get_version():
    """
    Get the current server version.
    """

    distribution = get_distribution()

    if distribution:
        return distribution.version

NAME = get_name() or 'Freelan server'
VERSION = get_version() or '0.0'

def register_version_information(app):
    """
    Register version-related methods to the specified Flask application.
    """

    @app.context_processor
    def add_version_information():
        """
        Makes the version available to the templating system.
        """

        return {
            'name': NAME,
            'version': VERSION,
        }
