"""
The user filters.
"""

from flask import render_template

def render_user_list(list_name, users):
    """
    Render a user list.
    """

    return render_template('elements/user_list.html', list_name=list_name, users=users)

def register_user_functions(app):
    """
    Register user-related functions to the specified Flask application.
    """

    @app.context_processor
    def add_user_functions():
        """
        Makes the user functions available to the templates.
        """

        return {
            'render_user_list': render_user_list,
        }
