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

def create_database(args):
    """
    Create the database.
    """

    from freelan_server.database import DATABASE, User

    DATABASE.create_all()

    DATABASE.session.add(User('admin', 'admin@admin.com', 'password', True))
    DATABASE.session.add(User('user', 'some@user.com', 'password'))
    DATABASE.session.commit()

def destroy_database(args):
    """
    Destroy the database.
    """

    from freelan_server.database import DATABASE

    DATABASE.drop_all()

def reset_database(args):
    """
    Destroy then create the database.
    """

    destroy_database()
    create_database()

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

    database_create_parser = database_action_parser.add_parser('create', help='Create the database if it doesn\'t exist yet.')
    database_create_parser.set_defaults(func=create_database)

    database_destroy_parser = database_action_parser.add_parser('destroy', help='Destroy the database.')
    database_destroy_parser.set_defaults(func=destroy_database)

    database_reset_parser = database_action_parser.add_parser('reset', help='Reset the database.')
    database_reset_parser.set_defaults(func=reset_database)

    # Parse the arguments
    args = parser.parse_args()
    args.func(args)
