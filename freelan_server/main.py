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

    from freelan_server.database import DATABASE, User

    DATABASE.init_all()

    DATABASE.session.add(User('admin', 'admin@admin.com', 'password', True))
    DATABASE.session.add(User('user', 'some@user.com', 'password'))
    DATABASE.session.commit()

def clean_database(args):
    """
    Clean the database.
    """

    from freelan_server.database import DATABASE

    DATABASE.drop_all()

def reset_database(args):
    """
    Clean then init the database.
    """

    clean_database()
    init_database()

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
    database_init_parser.set_defaults(func=init_database)

    database_clean_parser = database_action_parser.add_parser('clean', help='Clean the database.')
    database_clean_parser.set_defaults(func=clean_database)

    database_reset_parser = database_action_parser.add_parser('reset', help='Reset the database.')
    database_reset_parser.set_defaults(func=reset_database)

    # Parse the arguments
    args = parser.parse_args()
    args.func(args)
