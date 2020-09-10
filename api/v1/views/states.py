#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import Flask, jsonify, make_response, request, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    ''' Return list of all State objects'''
    states = storage.all(State)
    res = []
    for state in states.values():
        res.append(state.to_dict())
    return jsonify(res)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    ''' create state instance '''
    if not request.json:
        return 'Not a json', 400
    json_data = request.json
    if 'name' not in json_data:
        return 'Missing name', 400

    new_instance = State(**json_data)
    new_instance.save()

    return jsonify(new_instance.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    ''' Return State object '''
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    ''' Delete state id object '''
    states = storage.all(State).values()
    for state in states:
        print(state.id)
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    ''' update state instance by id '''
    if not request.json:
        return 'Not a json', 400
    json_data = request.json

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    dont = ['id', 'created_at', 'updadted_at']
    for key, value in json_data.items():
        if key not in dont:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
