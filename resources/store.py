import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores, items

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id], 200
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            for item in list(items.values()):  # can't delete values from dictionary during iteration
                if item["store_id"] == store_id:
                    del items[item["id"]]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}  # by default returns 200
        # stores.values() isn't a list it cannot turnned into json, therefore we convert to list.

    def post(self):
        store_data = request.get_json()
        store_id = uuid.uuid4().hex
        if "name" not in store_data:
            abort(400, message="Bad request. Ensure 'name' is included in the JSON payload")
        for store in stores.values():
            if store["name"] == store_data["name"]:
                abort(400, "Store already exist.")
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201
