#!/usr/bin/python3
"""
    Script that Create a new view for Amenity objects
    that handles all default RESTFul API actions:
"""
from flask import abort, request, jsonify
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def found_amenity():
    """
    The function "found_amenity" retrieves a list of amenities from
    storage and converts them into a list of dictionaries,
    which is then returned as a JSON response.
    """
    new_list_amenity = []
    list_amenity = storage.all("Amenity")
    for amenity in list_amenity.values():
        new_list_amenity.append(amenity.to_dict())
    return jsonify(new_list_amenity)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    The function `get_amenity_by_id` retrieves an amenity object from
    storage based on its ID and returns it as a JSON response.
    """
    list_amenity = storage.get("Amenity", str(amenity_id))
    if list_amenity is None:
        abort(404)

    return jsonify(list_amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    The function `delete_amenity` deletes an amenity object from
    storage based on its ID.
    """
    del_amenty = storage.get("Amenity", str(amenity_id))
    if del_amenty is None:
        abort(404)
    storage.delete(del_amenty)
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    The function creates a new amenity object using data from a JSON
    request and saves it to the database.
    """
    data_amenity = request.get_json(silent=True)
    if data_amenity is None:
        abort(400, "Not a JSON")
    if "name" not in data_amenity:
        abort(400, "Missing name")

    new_amenity = Amenity(**data_amenity)
    new_amenity.save()
    response = jsonify(new_amenity)
    response.status_code = 201
    return response


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    The function updates an amenity object with new data
    provided in a JSON format.
    """
    data_amenity = request.get_json(silent=True)
    if data_amenity is None:
        abort(404)
    fetch = storage.get("Amenity", str(amenity_id))
    if fetch is None:
        abort(400, "Not a JSON")
    for key, value in data_amenity.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetch, key, value)
    fetch.save()
    return jsonify(fetch.to_dict())
