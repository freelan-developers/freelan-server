"""
The freelan-server entry point.
"""

from flask import Flask, g

# Here goes the configuration
HOST = '::'
DEBUG = False

# We create an application
app = Flask(__name__)

app.config.from_object(__name__)
app.config.from_envvar('FREELAN_SERVER_CONFIGURATION_FILE', silent=True)

# Routes
@app.before_request
def before_request():
    g.user = 'me'

# We handle direct calls
if __name__ == '__main__':
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST']
    )
