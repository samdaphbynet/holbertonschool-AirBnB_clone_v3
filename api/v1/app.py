#!/usr/bin/python3
"""
    This is a Flask application that registers blueprints for API views
    and sets up a teardown function
    to close the storage context after the application context is torn down.
"""
from flask import Flask
import os
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app_context(exception):
    """
    The above function is a decorator that is used to close the storage
    context after the application
    context is torn down.
    """
    storage.close()


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
