"""
The views.
"""

from flask import redirect, url_for
from flask_login import login_required

from freelan_server.views.login import LoginView
from freelan_server.views.register import RegisterView
from freelan_server.views.logout import LogoutView
from freelan_server.views.settings_overview import SettingsOverviewView
from freelan_server.views.networks import NetworksView
from freelan_server.views.network import NetworkView, NetworkCreateView, NetworkDeleteView
from freelan_server.views.users import UsersView
from freelan_server.views.user import UserView, UserCreateView, UserDeleteView

from freelan_server.views.api.information import ApiInformationView
from freelan_server.views.api.login import ApiLoginView
from freelan_server.views.api.get_authority_certificate import ApiGetAuthorityCertificateView
from freelan_server.views.api.join_network import ApiJoinNetworkView
from freelan_server.views.api.sign import ApiSignView

@login_required
def root():
    """
    The root page.
    """

    return redirect(url_for('networks'))

def setup_views(app):
    """
    Setup the views of the specified Flask application.
    """

    app.add_url_rule('/', view_func=root, endpoint='root')
    app.add_url_rule('/register', view_func=RegisterView.as_view('register', app=app))
    app.add_url_rule('/login', view_func=LoginView.as_view('login', app=app))
    app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
    app.add_url_rule('/settings_overview', view_func=SettingsOverviewView.as_view('settings_overview', app=app))
    app.add_url_rule('/networks', view_func=NetworksView.as_view('networks'))
    app.add_url_rule('/network/create', view_func=NetworkCreateView.as_view('network/create'), methods=['GET', 'POST'])
    app.add_url_rule('/network/<int:network_id>', view_func=NetworkView.as_view('network'), methods=['GET', 'POST'])
    app.add_url_rule('/network/<int:network_id>/delete', view_func=NetworkDeleteView.as_view('network/delete'), methods=['POST'])
    app.add_url_rule('/users', view_func=UsersView.as_view('users'))
    app.add_url_rule('/user/create', view_func=UserCreateView.as_view('user/create'), methods=['GET', 'POST'])
    app.add_url_rule('/user/<int:user_id>', view_func=UserView.as_view('user'), methods=['GET', 'POST'])
    app.add_url_rule('/user/<int:user_id>/delete', view_func=UserDeleteView.as_view('user/delete'), methods=['POST'])
    app.add_url_rule('/api/information', view_func=ApiInformationView.as_view('api/information'), methods=['GET'])
    app.add_url_rule('/api/login', view_func=ApiLoginView.as_view('api/login'), methods=['GET', 'POST'])
    app.add_url_rule('/api/get_authority_certificate', view_func=ApiGetAuthorityCertificateView.as_view('api/get_authority_certificate', app=app), methods=['GET'])
    app.add_url_rule('/api/join_network', view_func=ApiJoinNetworkView.as_view('api/join_network', app=app), methods=['POST'])
    app.add_url_rule('/api/sign', view_func=ApiSignView.as_view('api/sign', app=app), methods=['POST'])
