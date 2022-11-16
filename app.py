import uuid

from flask import Flask, request
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

app = Flask(__name__)

# This is a Flask configuration that says that if there is an exception
# that occurs hidden inside an extension of Flask to propagate into the main app so that we can see it.
app.config["PROPAGATE_EXCEPTIONS"] = True
# flask_smorest configurations:
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
# telling flask_smorest which api documentation standard to use
app.config["OPENAPI_VERSION"] = "3.0.3"
# telling flask_smorest where is the root of the api
app.config["OPENAPI_URL_PREFIX"] = "/"
# documentaiton configurations
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)
