"""
The extensions.
"""

def register_all_extensions(app):
    """
    Register login-related methods to the specified Flask application.
    """

    # Register the login mechanism
    from freelan_server.extensions.login import register_login_information
    register_login_information(app)

    # Make the version information available to the templates
    from freelan_server.extensions.version import register_version_information
    register_version_information(app)

    # Make the menu information available to the templates
    from freelan_server.extensions.menu import register_menu_information
    register_menu_information(app)

    # Register the gravatar extension
    from freelan_server.extensions.gravatar import register_gravatar_filters
    register_gravatar_filters(app)

    # Register the user filters
    from freelan_server.extensions.user import register_user_functions
    register_user_functions(app)

    # Register the network filters
    from freelan_server.extensions.network import register_network_functions
    register_network_functions(app)

    # Register the crypto functions
    from freelan_server.extensions.crypto import register_crypto_functions
    register_crypto_functions(app)
