#!/usr/bin/python3
"""
    This is a Flask application that registers blueprints for API views
    and sets up a teardown function
    to close the storage context after the application context is torn down.
"""
from flask import Flask
from flask_cors import CORS
import os
from flask import jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app_context(exception):
    """
    The above function is a decorator that is used to close the storage
    context after the application
    context is torn down.
    """
    storage.close()


@app.errorhandler(404)
def page_not_find(ext):
    """
    The function returns a JSON response with an error message indicating that
    the page was not found.

    :param ext: The parameter "ext" is not used in the code snippet provided.
    It seems to be an unused
    parameter
    :return: a JSON response with an error message "Not found".
    """
    handler = {
            "error": "Not found"
            }
    res = jsonify(handler)
    res.status_code = 404
    return (res)


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
