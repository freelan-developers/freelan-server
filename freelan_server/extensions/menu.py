"""
The menu information
"""

MENU_ENTRIES = (
    {
        'url': 'networks',
        'title': 'Networks',
    },
    {
        'url': 'users',
        'title': 'Users',
    },
    {
        'url': 'settings',
        'title': 'Settings',
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
