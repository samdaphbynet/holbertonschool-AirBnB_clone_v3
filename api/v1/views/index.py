#!/usr/bin/python3
"""
    The `status` function returns a JSON response with the status "OK".
    :return: a JSON response with the status "OK".
"""


from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def object_by_type():
    """
    The function `object_by_type` returns a JSON object containing
    the count of different types of
    objects in a storage.
    :return: a JSON object that contains the counts of different types
    of objects in the storage. The
    counts include "amenities", "cities", "places", "reviews", "states",
    and "users".
    """
    return jsonify(
        {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
        })
