"""
The user view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template, abort
from flask_login import current_user, login_required
from freelan_server.database import DATABASE, User
from freelan_server.forms.user import UserForm

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

        if form.validate_on_submit():

            if (user == current_user) and form.new_password.data and not user.check_password(form.current_password.data):
                form.current_password.errors.append('Incorrect password.')
            else:
                form.populate_obj(user)

                # A new password was set, we need to update the user's one.
                if form.new_password.data:
                    user.password = form.new_password.data

                DATABASE.session.add(user)
                DATABASE.session.commit()

        return render_template('pages/user.html', form=form, user=user)

    get = get_or_post
    post = get_or_post

    def delete(self, user_id):
        return render_template('pages/user.html')

    def put(self):
        return render_template('pages/user.html')
