#!/usr/bin/python3
''' script that starts a Flask web application '''

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, render_template, Blueprint

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(error):
    ''' remove the current SQLAlchemy Session'''
    storage.close()


if __name__ == "__main__":

    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')

    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000

    app.run(host=host, port=port, threaded=True)
