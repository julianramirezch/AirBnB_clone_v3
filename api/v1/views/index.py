#!/usr/bin/python3

from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    ''' Returns status as json '''
    return jsonify({"status": "OK"})
