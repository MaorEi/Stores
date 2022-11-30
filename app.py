import os
import uuid

from flask import Flask, request
from flask_smorest import Api

from db import db
import models  # equivalent to import models.__init__
# our models need to be imported before we initialize the SQLAlchemy extension
# SQLAlchemy is gonna use our models to know what tables and columns to create when we tell it to create our tables for us.


from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint


# It's usually better to write a function whose job it is to create and set up and configure the Flask app.
# When we write tests for the Flask app we wanna call this function to get a new Flask App instead of running app.py.
# This is how to implement the Flask Factory Pattern
def create_app(db_url=None):
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

    # adding SQLAlchemy to the Flask app:
    # All DB providers (MySQL, Postgres, SQLite etc.) use a connection string that has all the necessary information for a client to connect to the DB.
    # This line is looking for the db url env variable, if it's not exist return sqlite by default
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL",
                                                                "sqlite:///data.db")  # sqlite:/// is a valid SQLite connection string that creates a file data.db and stores our data there.
    # environment variables are a good way to store arbitrary secrets or information in our server without storing them in our code.
    # for example; we don't want to store db connection strings in our code.
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Initializes the Flask SQLAlchemy extension, passing our Flask app that it can connect the Flask app to SQLAlchemy
    db.init_app(app)

    with app.app_context():
        # SQLAlchemy knows what tables to create because we've imported the models
        db.create_all()  # this is gonna run if the tables aren't already exist.

    api = Api(app)

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app
