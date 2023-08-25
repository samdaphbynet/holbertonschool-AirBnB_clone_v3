#!/usr/bin/python3
"""
    Script that Create a new view for user objects
    that handles all default RESTFul API actions:
"""
from flask import abort, request, jsonify
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def found_user():
    """
    The function "found_user" retrieves a list of users from
    storage and converts them into a list of dictionaries,
    which is then returned as a JSON response.
    """
    list_users = []
    users_get = storage.all("User")
    for user in users_get.values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """
    The function `get_user_by_id` retrieves an user object from
    storage based on its ID and returns it as a JSON response.
    """
    list_user = storage.get("User", str(user_id))
    if list_user is None:
        abort(404)

    return jsonify(list_user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """
    The function `delete_user` deletes an user object from
    storage based on its ID.
    """
    del_user = storage.get("User", str(user_id))
    if del_user is None:
        abort(404)
    storage.delete(del_user)
    storage.save()
    return jsonify({})


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    The function creates a new user object using data from a JSON
    request and saves it to the database.
    """
    data_user = request.get_json(silent=True)
    if data_user is None:
        abort(400, "Not a JSON")
    if "email" not in data_user:
        abort(400, "Missing email")
    if "password" not in data_user:
        abort(400, "Missing password")

    new_user = User(**data_user)
    new_user.save()
    response = jsonify(new_user.to_dict())
    response.status_code = 201
    return response


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """
    The function updates an user object with new data
    provided in a JSON format.
    """
    data_user = request.get_json(silent=True)
    if data_user is None:
        abort(400, "Not a JSON")
    fetch = storage.get("User", str(user_id))
    if fetch is None:
        abort(404)
    for key, value in data_user.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetch, key, value)
    fetch.save()
    return jsonify(fetch.to_dict())
