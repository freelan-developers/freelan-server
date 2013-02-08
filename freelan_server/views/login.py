"""
The login view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, login_user
from freelan_server.database import User
from freelan_server.forms.login import LoginForm

class LoginView(MethodView):
    """
    The login view.
    """

    def __init__(self, app):
        """
        Initialize the view.

        app is the application.
        """

        super(LoginView, self).__init__()

        self.app = app

    def get(self):

        form = LoginForm()

        if not self.app.config['RECAPTCHA_PRIVATE_KEY']:
            delattr(form, 'recaptcha')

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user and user.check_password(form.password.data):
                    session.regenerate()
                    login_user(user, remember=form.remember_me.data)

                    return redirect(url_for('root'))
            else:
                form.password.errors.append('The username or password is incorrect.')

        return render_template('pages/login.html', form=form, register_enabled=self.app.config['REGISTER_ENABLED'])

    post = get
