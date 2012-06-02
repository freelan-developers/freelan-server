"""
The library entry point.
"""

import os
import sys
from argparse import ArgumentParser

def run(args):
    """
    Run the webserver.
    """

    from freelan_server import APPLICATION

    APPLICATION.run(
        debug=APPLICATION.config['DEBUG'],
        host=APPLICATION.config['HOST']
    )

def init_database(args):
    """
    Initialize the database.
    """

    print 'Initializing the database...'

    from freelan_server.database import DATABASE, User

    DATABASE.create_all()

    if args.password:
        DATABASE.session.add(User('admin', 'admin@admin.com', args.password, True))
        print 'Added an "admin" account with the specified password.'
    else:
        DATABASE.session.add(User('admin', 'admin@admin.com', 'password', True))
        print 'Added an "admin" account with the default password "password".'

    if args.add_test_data:
        DATABASE.session.add(User('alice', 'alice@users.com', 'password'))
        DATABASE.session.add(User('bob', 'bob@users.com', 'password'))
        DATABASE.session.add(User('chris', 'chris@users.com', 'password'))
        DATABASE.session.add(User('denis', 'denis@users.com', 'password'))
        DATABASE.session.add(User('eleanor', 'eleanor@users.com', 'password'))
        print 'Added some user accounts with default password "password".'

    DATABASE.session.commit()

    print 'Database initialized.'

def clean_database(args):
    """
    Clean the database.
    """

    print 'Cleaning the database...'

    from freelan_server.database import DATABASE

    DATABASE.drop_all()

    print 'Database cleaned.'

def reset_database(args):
    """
    Clean then init the database.
    """

    clean_database(args)
    init_database(args)

def list_users(args):
    """
    List the users.
    """

    from freelan_server.database import User

    users = User.query.all()

    print 'Listing %s existing account(s):' % len(users)

    for user in users:
        print '%(type)s | %(username)s (%(email)s) created on %(creation_date)s' % {
            'type': user.admin_flag and 'admin' or 'user',
            'username': user.username,
            'email': user.email or '<no email>',
            'creation_date': user.creation_date,
        }

def main():
    """
    The entry point.
    """

    parser = ArgumentParser()

    # The subparsers
    action_parser = parser.add_subparsers()

    # The run parser
    run_parser = action_parser.add_parser('run', help='Run the web server')
    run_parser.set_defaults(func=run)

    # The database parser
    database_parser = action_parser.add_parser('database', help='Configure the database')
    database_action_parser = database_parser.add_subparsers()

    database_init_parser = database_action_parser.add_parser('init', help='Initialize the database if it doesn\'t exist yet.')
    database_init_parser.add_argument('-a', '--add-test-data', action='store_true', help='Add test users and networks to the database for testing.')
    database_init_parser.add_argument('-p', '--password', help='The password for the admin account.')
    database_init_parser.set_defaults(func=init_database)

    database_clean_parser = database_action_parser.add_parser('clean', help='Clean the database.')
    database_clean_parser.set_defaults(func=clean_database)

    database_reset_parser = database_action_parser.add_parser('reset', help='Reset the database.')
    database_reset_parser.add_argument('-a', '--add-test-data', action='store_true', help='Add test users and networks to the database for testing.')
    database_reset_parser.add_argument('-p', '--password', help='The password for the admin account.')
    database_reset_parser.set_defaults(func=reset_database)

    # The users parser
    users_parser = action_parser.add_parser('users', help='Manage the users')
    users_action_parser = users_parser.add_subparsers()

    users_list_parser = users_action_parser.add_parser('list', help='List the existing users.')
    users_list_parser.set_defaults(func=list_users)

    # Parse the arguments
    args = parser.parse_args()

    try:
        return args.func(args)
    except Exception, ex:
        print 'Error: %s' % ex
        return 1

