#!/usr/bin/python3
''' CRUD cities '''
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import Flask, jsonify, make_response, request, abort


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def list_cities(state_id):
    ''' Return list of all City objects'''
    states = storage.all(State)
    res = []
    if not states:
        abort(404)
    for state in states.values():
        for city in state.cities:
            res.append(city.to_dict())
    return jsonify(res)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    ''' create city instance '''
    state = storage.get(State, state_id)
    if not request.json:
        return 'Not a json', 400
    json_data = request.json
    if 'name' not in json_data:
        return 'Missing name', 400
    if not state:
        abort(404)

    json_data['state_id'] = state_id
    new_instance = City(**json_data)
    new_instance.save()

    return jsonify(new_instance.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    ''' Return City object '''
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    ''' Delete city id object '''
    cities = storage.all(City).values()
    for city in cities:
        print(city.id)
        if city.id == city_id:
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    ''' update city instance by id '''
    if not request.json:
        return 'Not a json', 400
    json_data = request.json

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    dont = ['id', 'created_at', 'updated_at', 'state_id']
    for key, value in json_data.items():
        if key not in dont:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
