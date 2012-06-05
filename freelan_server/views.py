"""
The views.
"""

from freelan_server import APPLICATION
from freelan_server.database import DATABASE, User, Network
from freelan_server.login import LOGIN_MANAGER, load_user
from freelan_server.gravatar import GRAVATAR
from sqlalchemy import desc, and_, or_, not_
from sqlalchemy.exc import OperationalError

from flask import g, session, request, redirect, abort, url_for, render_template, flash
from flask_login import login_required, login_user, logout_user, current_user

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
            ('settings', 'Settings'),
            ('status', 'Status'),
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

    return redirect(url_for('user', username=current_user.username))

@APPLICATION.route('/users')
@login_required
def users():
    """
    The users page.
    """

    users = User.query.order_by(desc(User.admin_flag)).order_by(User.username).all()

    return render_template('users.html', users=users)

@APPLICATION.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    """
    The user page.
    """

    user = User.query.filter_by(username=username).first()

    if not user:
        return abort(404);

    if request.method == 'POST':
        success = True
        email = request.form['email'] or ''
        password = request.form['password'] or ''
        new_password = request.form['new_password'] or ''
        new_password_repeat = request.form['new_password_repeat'] or ''
        admin_flag = ('admin_flag' in request.form)

        if new_password:
            if new_password != new_password_repeat:
                flash('New password and password repeat do not match.', 'error')
                success = False
            elif not user.check_password(password) and (not current_user.admin_flag or current_user.id == user.id):
                flash('Incorrect password.', 'error')
                success = False
            else:
                user.password = new_password

        if email and User.query.filter(and_(User.email == email, User.id != user.id)).first():
            flash('An user with the same email address already exists.', 'error')
            success = False

        if success:
            user.email = email

            if (current_user.id != user.id):
                user.admin_flag = admin_flag

            DATABASE.session.commit()

            flash('User "%s" was updated successfully.' % username, 'info')

            return redirect(url_for('users'))

    return render_template('user.html', user=user, referer={'target': 'users', 'title': 'Users'})

@APPLICATION.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    """
    The create user page.
    """

    if request.method == 'POST':
        username = request.form['username'] or ''
        email = request.form['email'] or ''
        password = request.form['password'] or ''
        password_repeat = request.form['password_repeat'] or ''
        admin_flag = ('admin_flag' in request.form)

        if not username:
            flash('Please specify an username.', 'error')
        elif not password:
            flash('Please specify a password.', 'error')
        elif password != password_repeat:
            flash('Password and password repeat do not match.', 'error')
        elif User.query.filter_by(username=username).first():
            flash('An user with the same username already exists.', 'error')
        elif email and User.query.filter_by(email=email).first():
            flash('An user with the same email address already exists.', 'error')
        else:
            user = User(username, email, password, admin_flag)
            DATABASE.session.add(user)
            DATABASE.session.commit()

            return redirect(url_for('users'))
    else:
        username = ''
        email = ''
        admin_flag = ''

    return render_template(
        'create_user.html',
        username=username,
        email=email,
        admin_flag=admin_flag,
        referer={'target': 'users', 'title': 'Users'},
    )

@APPLICATION.route('/delete_user/<username>', methods=['POST'])
@login_required
def delete_user(username):
    """
    The delete user page.
    """

    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No such user "%s".' % username, 'error')
    else:
        DATABASE.session.delete(user)
        DATABASE.session.commit()

        flash('User "%s" was deleted.' % username, 'info')

    return redirect(url_for('users'))

@APPLICATION.route('/networks')
@login_required
def networks():
    """
    The networks page.
    """

    networks = Network.query.order_by(Network.name).all()

    return render_template('networks.html', networks=networks)

@APPLICATION.route('/create_network', methods=['GET', 'POST'])
@login_required
def create_network():
    """
    The create network page.
    """

    return render_template(
        'create_network.html',
        referer={'target': 'networks', 'title': 'Networks'},
    )

@APPLICATION.route('/settings')
@login_required
def settings():
    """
    The settings page.
    """

    return render_template('settings.html')

@APPLICATION.route('/status')
@login_required
def status():
    """
    The status page.
    """

    return render_template('status.html')
