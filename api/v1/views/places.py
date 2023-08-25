#!/usr/bin/python3
"""
    Same as State, create a new view for place objects that
    handles all default RESTFul API actions:
"""
from flask import abort, jsonify, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def found_place(city_id):
    """
    The function "found_place" retrieves a list of cities associated with
    a given state ID and returns it as a JSON response.
    """
    list_place = []
    obj_place = storage.get("Place", str(city_id))
    if obj_place is None:
        abort(404)
    for key in obj_place.places:
        list_place.append(key.to_dict())
    return jsonify(list_place)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place_obj(place_id):
    """
    The function retrieves a place object from storage based on its ID and
    returns it as a JSON response.
    """
    obj_place = storage.get('Place', str(place_id))
    if obj_place is None:
        abort(404)
    return jsonify(obj_place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
    The function deletes a place object from storage based on its ID.
    """
    obj_place = storage.get("place", str(place_id))
    if obj_place is None:
        abort(404)
    storage.delete(obj_place)
    storage.save()
    return jsonify({})


@app_views.route("cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """
    The function creates a new place object and saves it to the database,
    returning the created place as a JSON response.
    """
    new_place = request.get_json(silent=True)
    if new_place is None:
        abort(400, "Not a JSON")

    if not storage.get("User", new_place["user_id"]):
        abort(404)

    if not storage.get("City", city_id):
        abort(404)

    if "user_id" not in new_place:
        abort(400, "Missing user_id")
    if "name" not in new_place:
        abort(400, "Missing name")

    new_place["city_id"] = city_id
    post_place = Place(**new_place)
    post_place.save()
    response = jsonify(post_place.to_dict())
    response.status_code = 201
    return response


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    The function updates the attributes of a place object based on
    the provided JSON data.
    """
    put_place = request.get_json(silent=True)

    if put_place is None:
        abort(400, "Not a JSON")

    fetch = storage.get("Place", str(place_id))

    if fetch is None:
        abort(404)

    for key, value in put_place.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fetch, key, value)
    fetch.save()
    return jsonify(fetch.to_dict())
