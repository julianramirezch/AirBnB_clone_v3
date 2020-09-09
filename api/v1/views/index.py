#!/usr/bin/python3

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    ''' Returns status as json '''
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count():
    '''  number of each objects by type '''
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'), 
        "states": storage.count('State'), 
        "users": storage.count('User'),
    }

    return jsonify(stats)
