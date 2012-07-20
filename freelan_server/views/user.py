"""
The user view.
"""

import re

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template, abort
from flask_login import current_user, login_required
from freelan_server.database import DATABASE, User
from freelan_server.forms.user import UserForm
from sqlalchemy.exc import IntegrityError

class UserView(MethodView):
    """
    The user view.
    """

    decorators = [login_required]

    def get_or_post(self, user_id):

        user = User.query.get(user_id)

        if not user:
            abort(404)

        form = UserForm(obj=user)

        # If we are editing a user that is not the current user, we don't need
        # to specify the current password.
        if user != current_user:
            del form.current_password

            if not current_user.admin_flag:
                del form.new_password
                del form.new_password_repeat
                del form.email

        if form.validate_on_submit():

            if (user == current_user) and form.new_password.data and not user.check_password(form.current_password.data):
                form.current_password.errors.append('Incorrect password.')
            else:
                if current_user != user and not current_user.admin_flag:
                    abort(403)

                form.populate_obj(user)

                # A new password was set, we need to update the user's one.
                if form.new_password.data:
                    user.password = form.new_password.data

                DATABASE.session.add(user)

                try:
                    DATABASE.session.commit()
                except IntegrityError as ex:
                    DATABASE.session.rollback()

                    m = re.search('column (\w+) is not unique', str(ex.orig))

                    attribute = m and m.group(1) or None

                    if hasattr(form, attribute):
                        form_attribute = getattr(form, attribute)
                    else:
                        form_attribute = form.username

                    form_attribute.errors.append('Database error: "%s".' % ex.orig)

        return render_template('pages/user.html', form=form, user=user)

    get = get_or_post
    post = get_or_post

    def delete(self, user_id):
        return render_template('pages/user.html')

    def put(self):
        return render_template('pages/user.html')
