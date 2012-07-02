"""
The menu information
"""

MENU_ENTRIES = (
    {
        'url': 'networks',
        'title': 'Networks',
        'icon': 'networks',
    },
    {
        'url': 'users',
        'title': 'Users',
        'icon': 'users',
    },
    {
        'url': 'settings_overview',
        'title': 'Settings',
        'icon': 'settings',
    },
#    {
#        'url': 'status',
#        'title': 'Status',
#    },
)

def register_menu_information(app):
    """
    Register menu-related methods to the specified Flask application.
    """

    @app.context_processor
    def add_menu_information():
        """
        Makes the menu available to the templating system.
        """

        return {
            'menu_entries': MENU_ENTRIES,
        }
