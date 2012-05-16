"""
The views.
"""

from freelan_server import APPLICATION
from freelan_server.database import DATABASE, User
from sqlalchemy.exc import OperationalError

from flask import g, redirect, url_for, render_template

@APPLICATION.route('/')
def home():
    """
    The home page.
    """

    try:
        users = User.query.all()

        return render_template('home.html', users=users)

    except OperationalError, ex:
        return render_template('no_database.html')

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

