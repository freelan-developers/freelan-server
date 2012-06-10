"""
The login view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, login_user
from freelan_server.database import User

class LoginView(MethodView):
    """
    The login view.
    """

    def render(self, login_error=None):
        """
        Render the login template.
        """

        return render_template('pages/login.html', login_error=login_error)

    def get(self):

        if current_user.is_authenticated():
            return redirect(url_for('root'))

        return self.render()

    def post(self):

        login_error = None

        username = request.form['username']
        password = request.form['password']
        remember = ('remember' in request.form) and (request.form['remember'] == 'yes')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
                session.regenerate()
                login_user(user, remember=remember)

                return redirect(request.args.get('next') or url_for('root'))
        else:
            login_error = 'The username or password is incorrect.'

        return self.render(login_error)
