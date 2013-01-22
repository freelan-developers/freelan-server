"""
The library entry point.
"""

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

    from freelan_server.database import DATABASE, User, Network

    DATABASE.create_all()

    if args.password:
        DATABASE.session.add(User('admin', 'admin@admin.com', args.password, True))
        print 'Added an "admin" account with the specified password.'
    else:
        DATABASE.session.add(User('admin', 'admin@admin.com', 'password', True))
        print 'Added an "admin" account with the default password "password".'

    if args.add_test_data:
        alice = User('alice', 'alice@users.com', 'password')
        bob = User('bob', 'bob@users.com', 'password')
        chris = User('chris', 'chris@users.com', 'password')
        denis = User('denis', 'denis@users.com', 'password')
        eleanor = User('eleanor', 'eleanor@users.com', 'password')

        DATABASE.session.add(alice)
        DATABASE.session.add(bob)
        DATABASE.session.add(chris)
        DATABASE.session.add(denis)
        DATABASE.session.add(eleanor)
        print 'Added some user accounts with default password "password".'

        my_network = Network('My network')
        foo_network = Network('Foo network')
        bar_network = Network('Bar network')
        virtual_network = Network('Virtual network')

        DATABASE.session.add(my_network)
        DATABASE.session.add(foo_network)
        DATABASE.session.add(bar_network)
        DATABASE.session.add(virtual_network)
        print 'Added some networks.'

        my_network.users.append(alice)
        my_network.users.append(bob)
        my_network.users.append(chris)
        foo_network.users.append(alice)
        foo_network.users.append(bob)
        bar_network.users.append(alice)
        virtual_network.users.append(chris)
        print 'Added some users to the networks.'

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

    from freelan_server.database import User, Network

    users = User.query.all()

    print 'Listing %s existing account(s):' % len(users)

    for user in users:
        print '%(type)s | %(username)s (%(email)s) created on %(creation_date)s | %(networks)s' % {
            'type': user.admin_flag and 'admin' or 'user',
            'username': user.username,
            'email': user.email or '<no email>',
            'creation_date': user.creation_date,
            'networks': ', '.join([network.name for network in user.networks])
        }

def list_users_memberships(args):
    """
    List the users memberships.
    """

    from freelan_server.database import User, Network

    if args.username:
        users = User.query.filter_by(username=args.username).all()

        if not users:
            print 'No such user: %s' % args.username
            return 1

        print 'Listing memberships for user: %s' % users[0].username

    else:
        users = User.query.all()

        print 'Listing memberships for %s existing account(s):' % len(users)

    for user in users:
        print

        if user.networks:
            print u'%s:' % user.username

            if args.network:
                networks = Network.query.filter_by(name=args.network).all()

                if not networks:
                    print 'No such network: %s' % args.network

            else:
                networks = user.networks

            for network in networks:
                active_memberships = user.get_active_memberships(network)

                if active_memberships:
                    print u'* %s: %s' % (network.name, ', '.join(x.endpoint for x in active_memberships))
                else:
                    print u'* %s: no memberships' % network.name
        else:
            print u'%s: no networks' % user.username

def create_user(args):
    """
    Create a user.
    """

    from freelan_server.database import DATABASE, User

    DATABASE.session.add(User(args.username, args.email, args.password, args.admin))
    DATABASE.session.commit()

    print 'The user was created.'

def delete_user(args):
    """
    Delete a user.
    """

    from freelan_server.database import DATABASE, User

    user = User.query.filter_by(username=args.username).first()

    if user:
        DATABASE.session.delete(user)
        DATABASE.session.commit()

        print 'User "%s" was successfully deleted.' % args.username
    else:
        print 'User "%s" does not exist.' % args.username
        return 1

def update_user(args):
    """
    Update a user.
    """

    from freelan_server.database import DATABASE, User

    user = User.query.filter_by(username=args.username).first()

    if user:
        if args.password is not None:
            user.password = args.password
            print 'Password updated for user "%s".' % args.username

        if args.email is not None:
            if args.email:
                user.email = args.email
                print 'Email address updated for user "%s".' % args.username
            else:
                user.email = None
                print 'Email address reset for user "%s".' % args.username

        # FIXME: If the -a option is not specified, the admin status always gets reset.
        if args.admin is not None:
            user.admin_flag = args.admin

            if args.admin:
                print 'Admin status set for user "%s".' % args.username
            else:
                print 'Admin status reset for user "%s".' % args.username

        DATABASE.session.commit()
    else:
        print 'User "%s" does not exist.' % args.username
        return 1

def list_networks(args):
    """
    List the networks.
    """

    from freelan_server.database import User, Network

    networks = Network.query.all()

    print 'Listing %s existing network(s):' % len(networks)

    for network in networks:
        print '%(name)s | %(users_len)s user(s). Created on %(creation_date)s | %(users)s | %(ipv4_address)s | %(ipv6_address)s' % {
            'name': network.name,
            'creation_date': network.creation_date,
            'users_len': len(network.users),
            'users': ', '.join([user.username for user in network.users]),
            'ipv4_address': network.ipv4_address or 'No IPv4 address',
            'ipv6_address': network.ipv6_address or 'No IPv6 address',
        }

def create_network(args):
    """
    Create a network.
    """

    from freelan_server.database import DATABASE, Network

    DATABASE.session.add(Network(args.name))
    DATABASE.session.commit()

    print 'The network was created.'

def delete_network(args):
    """
    Delete a network.
    """

    from freelan_server.database import DATABASE, Network

    network = Network.query.filter_by(name=args.name).first()

    if network:
        DATABASE.session.delete(network)
        DATABASE.session.commit()

        print 'Network "%s" was successfully deleted.' % args.name
    else:
        print 'Network "%s" does not exist.' % args.name
        return 1

def update_network(args):
    """
    Update a network.
    """

    from freelan_server.database import DATABASE, Network

    network = Network.query.filter_by(name=args.name).first()

    if network:
        # TODO: Something, probably
        DATABASE.session.commit()
    else:
        print 'Network "%s" does not exist.' % args.name
        return 1

def rename_network(args):
    """
    Rename a network.
    """

    from freelan_server.database import DATABASE, Network

    network = Network.query.filter_by(name=args.name).first()

    if network:
        network.name = args.newname

        DATABASE.session.commit()
        print 'Network "%s" was renamed to "%s".' % (args.name, args.newname)
    else:
        print 'Network "%s" does not exist.' % args.name
        return 1

def adduser_network(args):
    """
    Add a user to the network.
    """

    from freelan_server.database import DATABASE, User, Network

    network = Network.query.filter_by(name=args.name).first()

    if not network:
        print 'Network "%s" does not exist.' % args.name
        return 1

    user = User.query.filter_by(username=args.username).first()

    if not user:
        print 'User "%s" does not exist.' % args.username
        return 1

    if user in network.users:
        print 'User "%s" already belongs to "%s".' % (args.username, args.name)
        return 1

    network.users.append(user)

    DATABASE.session.commit()

def removeuser_network(args):
    """
    Remove a user from the network.
    """

    from freelan_server.database import DATABASE, User, Network

    network = Network.query.filter_by(name=args.name).first()

    if not network:
        print 'Network "%s" does not exist.' % args.name
        return 1

    user = User.query.filter_by(username=args.username).first()

    if not user:
        print 'User "%s" does not exist.' % args.username
        return 1

    if not user in network.users:
        print 'User "%s" does not belong to "%s".' % (args.username, args.name)
        return 1

    network.users.remove(user)

    DATABASE.session.commit()

def main():
    """
    The entry point.
    """

    parser = ArgumentParser()

    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')

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

    # The user parser
    user_parser = action_parser.add_parser('user', help='Manage the users')
    user_action_parser = user_parser.add_subparsers()

    user_list_parser = user_action_parser.add_parser('list', help='List the existing users.')
    user_list_parser.set_defaults(func=list_users)

    user_membership_parser = user_action_parser.add_parser('membership', help='List the existing users memberships.')
    user_membership_parser.set_defaults(func=list_users_memberships)
    user_membership_parser.add_argument('-u', '--username', help='The user username to filter with.')
    user_membership_parser.add_argument('-n', '--network', help='The network name to filter with.')

    user_create_parser = user_action_parser.add_parser('create', help='Create a user.')
    user_create_parser.add_argument('username', help='The user username.')
    user_create_parser.add_argument('password', help='The user password.')
    user_create_parser.add_argument('-e', '--email', help='The user email.')
    user_create_parser.add_argument('-a', '--admin', action='store_true', help='The user admin flag.')
    user_create_parser.set_defaults(func=create_user)

    user_delete_parser = user_action_parser.add_parser('delete', help='Delete a user.')
    user_delete_parser.add_argument('username', help='The username of the user to delete.')
    user_delete_parser.set_defaults(func=delete_user)

    user_update_parser = user_action_parser.add_parser('update', help='Update a user.')
    user_update_parser.add_argument('username', help='The user username.')
    user_update_parser.add_argument('-p', '--password', help='The user password.')
    user_update_parser.add_argument('-e', '--email', nargs='?', const='', help='The user email. Specify an empty value or no value to delete the email address.')

    user_update_parser_admin_group = user_update_parser.add_mutually_exclusive_group(required=False)
    user_update_parser_admin_group.add_argument('-a', '--admin', action='store_true', dest='admin', help='Set the user admin flag.')
    user_update_parser_admin_group.add_argument('-u', '--user', action='store_false', dest='admin', help='Reset the user admin flag.')
    user_update_parser.set_defaults(func=update_user)

    # The network parser
    network_parser = action_parser.add_parser('network', help='Manage the networks')
    network_action_parser = network_parser.add_subparsers()

    network_list_parser = network_action_parser.add_parser('list', help='List the existing networks.')
    network_list_parser.set_defaults(func=list_networks)

    network_create_parser = network_action_parser.add_parser('create', help='Create a network.')
    network_create_parser.add_argument('name', help='The network name.')
    network_create_parser.set_defaults(func=create_network)

    network_delete_parser = network_action_parser.add_parser('delete', help='Delete a network.')
    network_delete_parser.add_argument('name', help='The name of the network to delete.')
    network_delete_parser.set_defaults(func=delete_network)

    network_update_parser = network_action_parser.add_parser('update', help='Update a network.')
    network_update_parser.add_argument('name', help='The network name.')
    network_update_parser.set_defaults(func=update_network)

    network_update_parser = network_action_parser.add_parser('rename', help='Rename a network.')
    network_update_parser.add_argument('name', help='The current network name.')
    network_update_parser.add_argument('newname', help='The new network name.')
    network_update_parser.set_defaults(func=rename_network)

    network_update_parser = network_action_parser.add_parser('adduser', help='Add a user to the network.')
    network_update_parser.add_argument('username', help='The username.')
    network_update_parser.add_argument('name', help='The network name.')
    network_update_parser.set_defaults(func=adduser_network)

    network_update_parser = network_action_parser.add_parser('removeuser', help='Remove a user from the network.')
    network_update_parser.add_argument('username', help='The username.')
    network_update_parser.add_argument('name', help='The network name.')
    network_update_parser.set_defaults(func=removeuser_network)

    # Parse the arguments
    args = parser.parse_args()

    try:
        return args.func(args)

    except Exception, ex:
        if args.debug:
            raise
        else:
            print 'Error: %s' % ex

        return 1
