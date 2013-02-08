"""
The register view.
"""

from flask.views import MethodView

from flask import redirect, url_for, request, session, render_template
from flask_login import current_user, login_user
from freelan_server.database import DATABASE, User
from freelan_server.forms.register import RegisterForm

class RegisterView(MethodView):
    """
    The register view.
    """

    def __init__(self, app):
        """
        Initialize the view.

        app is the application.
        """

        super(RegisterView, self).__init__()

        self.app = app

    def get(self):

        if not self.app.config['REGISTER_ENABLED']:
            return 'Registration is disabled on this server.', 403

        if not current_user.is_anonymous():
            return 'You can\'t register a new user as an already register user.', 403

        user = User()

        form = RegisterForm(obj=user)

        if not self.app.config['RECAPTCHA_PRIVATE_KEY']:
            delattr(form, 'recaptcha')

        if form.validate_on_submit():

            form.populate_obj(user)

            DATABASE.session.add(user)

            try:
                DATABASE.session.commit()

                session.regenerate()
                login_user(user, remember=False)

                return redirect(url_for('root'))
            except IntegrityError as ex:
                DATABASE.session.rollback()

                m = re.search('column (\w+) is not unique', str(ex.orig))

                attribute = m and m.group(1) or None

                if hasattr(form, attribute):
                    form_attribute = getattr(form, attribute)
                else:
                    form_attribute = form.username

                form_attribute.errors.append('Database error: "%s".' % ex.orig)

        return render_template('pages/register.html', form=form)

    post = get
