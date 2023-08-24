#!/usr/bin/python3
"""
    Same as State, create a new view for City objects that
    handles all default RESTFul API actions:
"""
from flask import abort, jsonify, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def found_city(state_id):
    """
    The function "found_city" retrieves a list of cities associated with
    a given state ID and returns it as a JSON response.
    """
    list_cities = []
    obj_state = storage.get("State", state_id)
    if obj_state is None:
        abort(404)
    for key in obj_state.cities:
        list_cities.append(key.to_dict())
    return jsonify(list_cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city_obj(city_id):
    """
    The function retrieves a city object from storage based on its ID and
    returns it as a JSON response.
    """
    obj_city = storage.get('City', str(city_id))
    if obj_city is None:
        abort(404)
    return jsonify(obj_city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    The function deletes a city object from storage based on its ID.
    """
    obj_city = storage.get("City", str(city_id))
    if obj_city is None:
        abort(404)
    storage.delete(obj_city)
    storage.save()
    return jsonify({})


@app_views.route("states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """
    The function creates a new city object and saves it to the database,
    returning the created city as a JSON response.
    """
    new_city = request.get_json(silent=True)
    if new_city is None:
        abort(400, "Not a JSON")

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in new_city:
        abort(400, "Missing name")

    new_city["state_id"] = state_id
    post_city = City(**new_city)
    post_city.save()
    response = jsonify(post_city.to_dict())
    response.status_code = 201
    return response


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    The function updates the attributes of a city object based on
    the provided JSON data.
    """
    put_city = request.get_json(silent=True)
    if put_city is None:
        abort(400, "Not a JSON")
    fetch = storage.get("City", str(city_id))
    if fetch is None:
        abort(404)
    for key, value in put_city.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fetch, key, value)
    fetch.save()
    return jsonify(fetch.to_dict())
