#!/usr/bin/python3
''' CRUD places '''
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import Flask, jsonify, make_response, request, abort


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def list_places(city_id):
    ''' Return list of all Place objects'''
    city = storage.get(City, city_id)
    res = []
    if not city:
        abort(404)
    for place in city.places:
        res.append(place.to_dict())
    return jsonify(res)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    ''' create Place instance '''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        return 'Not a JSON', 400
    json_data = request.json
    if 'user_id' not in json_data:
        return 'Missing user_id', 400
    user = storage.get(User, json_data['user_id'])
    if not user:
        abort(404)
    if 'name' not in json_data:
        return 'Missing name', 400

    json_data['city_id'] = city_id
    new_instance = Place(**json_data)
    new_instance.save()

    return jsonify(new_instance.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    ''' Return Place object '''
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_Place(place_id):
    ''' Delete Place id object '''
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_Place(place_id):
    ''' update Place instance by id '''
    if not request.json:
        return 'Not a JSON', 400
    json_data = request.json

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    dont = ['id', 'created_at', 'updated_at', 'place_id']
    for key, value in json_data.items():
        if key not in dont:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
