from setuptools import setup

setup(
    name='Freelan Server',
    version='1.0',
    long_description=__doc__,
    packages=[
        'freelan_server',
        'freelan_server.database',
        'freelan_server.extensions',
        'freelan_server.forms',
        'freelan_server.views',
        'freelan_server.views.api',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'SQLAlchemy',
        'Flask-SQLAlchemy',
        'Flask-Login',
        'Flask-KVSession',
        'Flask-Gravatar',
        'Flask-WTF',
        'M2Crypto',
        'IPy',
    ],
    entry_points = {
        'console_scripts': [
            'freelan_server = freelan_server.main:main',
        ],
    },
)
