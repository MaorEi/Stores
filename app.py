import uuid

from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 200
    except KeyError:
        abort(404, message="Store not found.")


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}  # by default returns 200
    # stores.values() isn't a list it cannot turnned into json, therefore we convert to list.


@app.post("/store")
def create_store():
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


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        for item in list(items.values()):  # can't delete values from dictionary during iteration
            if item["store_id"] == store_id:
                del items[item["id"]]
        return {"message": "Store deleted"}
    except KeyError:
        abort(404, message="Store not found.")


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        abort(404, message="Item not found.")


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if "price" not in item_data or "store_id" not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload")
    for item in items.values():
        if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
            abort(400, "Item already exists.")
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload")
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message="Item not found.")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")
