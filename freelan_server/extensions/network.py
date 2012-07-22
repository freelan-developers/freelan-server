"""
The network filters.
"""

from flask import render_template

from jinja2 import Markup

def render_network_list(list_name, networks):
    """
    Render a network list.
    """

    return Markup(render_template('elements/network_list.html', list_name=list_name, networks=networks))

def register_network_functions(app):
    """
    Register network-related functions to the specified Flask application.
    """

    @app.context_processor
    def add_network_functions():
        """
        Makes the network functions available to the templates.
        """

        return {
            'render_network_list': render_network_list,
        }
