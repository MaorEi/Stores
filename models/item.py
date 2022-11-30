from db import db


# Any class that we create that maps to a table with columns
# SQLAlchemy will automatically turn the table rows into Python objects.
class ItemModel(db.Model):
    __tablename__ = "items"  # tells SQLAlchemy that we wanna create or use a table called items for this class
    id = db.Column(db.Integer, primary_key=True)  # if we use Postgres it'll make it auto-incrementing key
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False,
                         nullable=False)  # one-to-many relationship
    store = db.relationship("StoreModel", back_populates="items")
    # SQLAlchemy knows the stores table is used by the StoreModel class,
    # The relationship with the StoreModel class will automatically populate the store variable with a StoreModel object
