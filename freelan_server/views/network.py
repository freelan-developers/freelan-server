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

def create_form(network=None):
    """
    Create a form.
    """

    form = NetworkForm(obj=network)

    return form

class NetworkView(MethodView):
    """
    The network view.
    """

    decorators = [login_required]

    def get(self, network_id):

        network = Network.query.get(network_id)

        if not network:
            abort(404)

        form = create_form(network)

        return render_template('pages/network.html', form=form, network=network)

    def post(self, network_id):

        if not current_user.admin_flag:
            abort(403)

        network = Network.query.get(network_id)

        if not network:
            abort(404)

        form = create_form(network)

        if form.validate_on_submit():

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

class NetworkCreateView(MethodView):
    """
    The network create view.
    """

    decorators = [login_required]

    def get(self):

        if not current_user.admin_flag:
            abort(403)

        form = create_form()

        return render_template('pages/network.html', form=form, network=None)

    def post(self):

        if not current_user.admin_flag:
            abort(403)

        network = None

        form = create_form()

        if form.validate_on_submit():
            network = Network()

            form.populate_obj(network)

            DATABASE.session.add(network)

            try:
                DATABASE.session.commit()
            except IntegrityError as ex:
                network = None
                DATABASE.session.rollback()

                m = re.search('column (\w+) is not unique', str(ex.orig))

                attribute = m and m.group(1) or None

                if hasattr(form, attribute):
                    form_attribute = getattr(form, attribute)
                else:
                    form_attribute = form.name

                form_attribute.errors.append('Database error: "%s".' % ex.orig)

        return render_template('pages/network.html', form=form, network=network)

class NetworkDeleteView(MethodView):
    """
    The network delete view.
    """

    decorators = [login_required]

    def post(self, network_id):

        if not current_user.admin_flag:
            abort(403)

        network = Network.query.get(network_id)

        if not network:
            abort(404)

        DATABASE.session.delete(network)
        DATABASE.session.commit()

        return redirect(url_for('networks'))
