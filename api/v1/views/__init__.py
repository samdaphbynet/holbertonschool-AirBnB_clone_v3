# This code is creating a Flask Blueprint object named `app_views`. A Blueprint is a way to organize
# related routes and views in a Flask application.
from flask import Blueprint
app_views = Blueprint("/api/v1", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
