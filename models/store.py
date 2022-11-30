from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")
    # This relationship allows each StoreModel to see very easily all the ItemModels associated with it.
    # dynamic laziness means that the items aren't gonna be fetched from the DB until we tell it to. it's not gonna prefetch them

