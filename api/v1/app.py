#!/usr/bin/python3
''' script that starts a Flask web application '''

from os import getenv
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from flask import Flask, render_template, Blueprint, make_response, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(error):
    ''' remove the current SQLAlchemy Session'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":

    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')

    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000

    app.run(host=host, port=port, threaded=True)
