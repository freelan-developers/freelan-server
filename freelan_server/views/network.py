"""
The network view.
"""

import re

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template, abort
from flask_login import current_user, login_required
from freelan_server.database import DATABASE, Network
from freelan_server.forms.network import NetworkForm
from sqlalchemy.exc import IntegrityError

class NetworkView(MethodView):
    """
    The network view.
    """

    decorators = [login_required]

    def get_or_post(self, network_id):

        network = Network.query.get(network_id)

        if not network:
            abort(404)

        form = NetworkForm(obj=network)

        if form.validate_on_submit():

            if not current_user.admin_flag:
                abort(403);

            form.populate_obj(network)

            DATABASE.session.add(network)

            try:
                DATABASE.session.commit()
            except IntegrityError as ex:
                DATABASE.session.rollback()

                m = re.search('column (\w+) is not unique', str(ex.orig))

                attribute = m and m.group(1) or None

                if hasattr(form, attribute):
                    form_attribute = getattr(form, attribute)
                else:
                    form_attribute = form.name

                form_attribute.errors.append('Database error: "%s".' % ex.orig)

        return render_template('pages/network.html', form=form, network=network)

    get = get_or_post
    post = get_or_post

    def delete(self, network_id):
        return render_template('pages/network.html')

    def put(self):
        return render_template('pages/network.html')
