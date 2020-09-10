#!/usr/bin/python3
''' CRUD places '''
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from flask import Flask, jsonify, make_response, request, abort


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def list_reviews(place_id):
    ''' Return list of all Place objects'''
    place = storage.get(Place, place_id)
    res = []
    if not place:
        abort(404)
    for review in place.reviews:
        res.append(review.to_dict())
    return jsonify(res)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    ''' create Place instance '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        return 'Not a JSON', 400
    json_data = request.json
    if 'user_id' not in json_data:
        return 'Missing user_id', 400
    user = storage.get(User, json_data['user_id'])
    if not user:
        abort(404)
    if 'text' not in json_data:
        return 'Missing text', 400

    json_data['place_id'] = place_id
    new_instance = Review(**json_data)
    new_instance.save()

    return jsonify(new_instance.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    ''' Return Place object '''
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    ''' Delete Place id object '''
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.id == review_id:
            storage.delete(review)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    ''' update Place instance by id '''
    if not request.json:
        return 'Not a JSON', 400
    json_data = request.json

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    dont = ['id', 'created_at', 'updated_at', 'place_id', 'user_id']
    for key, value in json_data.items():
        if key not in dont:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
