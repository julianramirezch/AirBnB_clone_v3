#!/usr/bin/python3
''' CRUD users '''
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import Flask, jsonify, make_response, request, abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    ''' Return list of all User objects'''
    users = storage.all(User)
    res = []
    for user in users.values():
        res.append(user.to_dict())
    return jsonify(res)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    ''' create user instance '''
    if not request.json:
        return 'Not a json', 400
    json_data = request.json
    if 'email' not in json_data:
        return 'Missing email', 400
    if 'password' not in json_data:
        return 'Missing password', 400
    new_instance = User(**json_data)
    new_instance.save()

    return jsonify(new_instance.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    ''' Return User object '''
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    ''' Delete user id object '''
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            storage.delete(user)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    ''' update user instance by id '''
    if not request.json:
        return 'Not a json', 400
    json_data = request.json

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    dont = ['id', 'email', 'created_at', 'updadted_at']
    for key, value in json_data.items():
        if key not in dont:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
