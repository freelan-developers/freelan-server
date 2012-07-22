"""
The networks view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, login_required

from freelan_server.database import Network

class NetworksView(MethodView):
    """
    The networks view.
    """

    decorators = [login_required]

    def get(self):

        networks = Network.query.order_by(Network.name).all()

        return render_template('pages/networks.html', networks=networks)
