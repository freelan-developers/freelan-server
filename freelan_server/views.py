"""
The views.
"""

from freelan_server import APPLICATION
from freelan_server.database import DATABASE, User
from freelan_server.login import LOGIN_MANAGER, load_user
from sqlalchemy.exc import OperationalError

from flask import g, session, request, redirect, url_for, render_template, flash
from flaskext.login import login_required, login_user, logout_user, current_user

@APPLICATION.route('/')
@login_required
def home():
    """
    The home page.
    """

    try:
        tiles = (
            ('users', 'Users'),
            ('networks', 'Networks'),
            ('profile', 'Profile'),
            ('logout', 'Logout'),
        )

        return render_template('home.html', tiles=tiles)

    except OperationalError, ex:
        return render_template('no_database.html')

@APPLICATION.route('/login', methods=['GET', 'POST'])
def login():
    """
    The login page.
    """

    if current_user.is_authenticated():
        return redirect(url_for('home'))

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

@APPLICATION.route('/logout')
def logout():
    """
    The logout page.
    """
    if current_user.is_authenticated():
        flash('You are not longer logged in.', 'info')

    logout_user()

    return redirect(url_for('login'))

@APPLICATION.route('/profile')
@login_required
def profile():
    """
    The profile page.
    """

    return render_template('profile.html')

@APPLICATION.route('/users')
@login_required
def users():
    """
    The users page.
    """

    return render_template('users.html')

@APPLICATION.route('/networks')
@login_required
def networks():
    """
    The networks page.
    """

    return render_template('networks.html')

# TODO: Remove/adapt the calls below as they are only provided for development

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

