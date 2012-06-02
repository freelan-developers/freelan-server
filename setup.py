from setuptools import setup

setup(
    name='Freelan Server',
    version='1.0',
    long_description=__doc__,
    packages=['freelan_server'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'SQLAlchemy',
        'Flask-Login',
        'Flask-KVSession',
        'Flash-Gravatar',
    ],
)
