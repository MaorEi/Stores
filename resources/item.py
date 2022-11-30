import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError  # SQLAlchemy is the base error

from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

from db import db

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # Flask SQLAlchemy is giving us the query attribute from the db.Model
        # Using only vanilla SQLAlchemy won't give us the handy query attribute.
        # get_or_404 retrieves the data by the primary key if there isn't a matched item it'll automatically abort with 404 status code
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Item {item_id} deleted"}
        # raise NotImplementedError("Deleting an item isn't implemented")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,
                  ItemSchema)  # Note: the decorators order matters, ensure blp.response to be deeper as possible.
    def put(self, item_data, item_id):  # Note: the request body json always come first before other route arguments
        item = ItemModel.query.get(item_id)
        # Note: we want to implement idempotency in our API.
        # idempotent request means that running one or more requests should result the same state at the end of it.
        # It makes sure the client can't mess things up by sending two requests instead of one, if they do that accidentally.
        # It's a very common feature in a PUT request.
        if item:  # if exists update
            item.price = item_data["price"]
            item.name = item_data["name"]
            item.store_id = item_data["store_id"]  # TODO: how to implement partial updates in Flask
        else:  # otherwise create a new item
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/item")
class ItemList(MethodView):
    # the all() method will return a cursor and the ItemSchema(many=True) will return it as a list of items
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)  # the db.session.add put the data in a place where it's not written into the db file
            db.session.commit()  # but it will be written in the db file when we commit.
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item")
        return item
