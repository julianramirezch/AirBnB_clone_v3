#!/usr/bin/python3
''' CRUD amenities '''
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import Flask, jsonify, make_response, request, abort


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenities():
    ''' Return list of all Amenity objects'''
    amenities = storage.all(Amenity)
    res = []
    for amenity in amenities.values():
        res.append(amenity.to_dict())
    return jsonify(res)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    ''' create amenity instance '''
    if not request.json:
        return 'Not a json', 400
    json_data = request.json
    if 'name' not in json_data:
        return 'Missing name', 400

    new_instance = Amenity(**json_data)
    new_instance.save()

    return jsonify(new_instance.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    ''' Return Amenity object '''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    ''' Delete amenity id object '''
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        print(amenity.id)
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    ''' update amenity instance by id '''
    if not request.json:
        return 'Not a json', 400
    json_data = request.json

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    dont = ['id', 'created_at', 'updadted_at']
    for key, value in json_data.items():
        if key not in dont:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
