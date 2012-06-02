"""
The views.
"""

from freelan_server import APPLICATION
from freelan_server.database import DATABASE, User
from freelan_server.login import LOGIN_MANAGER, load_user
from sqlalchemy.exc import OperationalError

from flask import g, session, request, redirect, url_for, render_template, flash
from flaskext.login import login_required, login_user

@APPLICATION.route('/')
@login_required
def home():
    """
    The home page.
    """

    try:
        users = User.query.all()

        return render_template('home.html', users=users)

    except OperationalError, ex:
        return render_template('no_database.html')

@APPLICATION.route('/login', methods=['GET', 'POST'])
def login():
    """
    The login page.
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = ('remember' in request.form) and (request.form['remember'] == 'yes')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
                session.regenerate()
                login_user(user, remember=remember)

                flash('Authentication successful.', 'info')

                return redirect(request.args.get('next') or url_for('home'))
        else:
            flash('Authentication failed for user "%s".' % username, 'denied')

    return render_template('login.html')

@APPLICATION.route('/create_database')
def create_database():
    """
    Create the database.
    """

    DATABASE.create_all()

    DATABASE.session.add(User('admin', None, 'password'))
    DATABASE.session.add(User('user', None, 'password'))
    DATABASE.session.commit()

    return redirect(url_for('home'))

@APPLICATION.route('/destroy_database')
def destroy_database():
    """
    Destroy the database.
    """

    DATABASE.drop_all()

    return redirect(url_for('home'))

