"""
The version information.
"""

VERSION = '1.0'

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
            'version': VERSION,
        }
