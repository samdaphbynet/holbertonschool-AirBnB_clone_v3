#!/usr/bin/python3
"""
    Script that create a new view for State objects that handles
    all default RESTFul API actions:
"""
from flask import abort, jsonify, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_state():
    """
    The function `get_state` retrieves a list of state objects from storage
    and converts them to
    dictionaries, then returns the list as a JSON response.
    :return: a JSON response containing a list of dictionaries representing
    the state objects.
    """
    state_list = []
    list_obj = storage.all("State")
    for obj in list_obj.values():
        state_list.append(obj.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_id(state_id):
    """
    The function retrieves a state object from storage based on its ID and
    returns it as a JSON response.
    """
    fetch = storage.get("State", str(state_id))
    if fetch is None:
        abort(404)
    return jsonify(fetch.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_by_id(state_id):
    """
    The function deletes a state object from storage based on its ID.

    :param state_id: The state_id parameter is the unique identifier
    of the state that you want to
    delete from the storage
    :return: An empty JSON object is being returned.
    """
    fetch = storage.get("State", str(state_id))
    if fetch is None:
        abort(404)
    storage.delete(fetch)
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_post():
    """
    The function `state_post` receives a JSON object,checks if it is valid,
    creates a new State object
    from the JSON, saves it, and returns a JSON response
    :return: a JSON response with the newly created state object in the body.
    The status code of the
    response is set to 201, indicating that the request was successful.
    """
    post_json = request.get_json(silent=True)
    if post_json is None:
        abort(400, "Not a JSON")
    if "name" not in post_json:
        abort(400, "Missing name")
    new_state = State(**post_json)
    new_state.save()
    response = jsonify(new_state.to_dict())
    response.status_code = 201
    return response


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    The function updates the state information with the provided state
    ID using the state_update JSON
    data.

    :param state_id: The `state_id` parameter is the identifier of the state
    that needs to be updated.
    It is used to fetch the existing state from the storage
    :return: a JSON representation of the updated state object.
    """
    state_update = request.get_json(silent=True)
    if state_update is None:
        abort(400, "Not a JSON")
    fetch = storage.get("State", str(state_id))
    if fetch is None:
        abort(404)
    for key, value in state_update.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetch, key, value)
    fetch.save()
    return jsonify(fetch.to_dict())
