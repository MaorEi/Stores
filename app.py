import uuid

from flask import Flask, request
from db import items, stores

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}  # by default returns 200
    # stores.values() isn't a list it cannot turnned into json, therefore we convert to list.


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 400
    item_id = uuid.uuid4().hex
    item = {**item_id, "id": item_id}
    items[item_id] = item
    return item, 201


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 200
    except KeyError:
        return {"message": "store doesn't exist"}, 400


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        return {"message": "item doesn't exist"}, 400

@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201

