#!/usr/bin/python3
"""
    The `status` function returns a JSON response with the status "OK".
    :return: a JSON response with the status "OK".
"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})
