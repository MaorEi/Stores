from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Str(dump_only=True)  # We only want to use it for returning data.
    name = fields.Str(required=True)  # This field is required both ends (getting & returning) and checks if is String.
    price = fields.Float(required=True)  # This field is required and checks if is Float.
    store_id = fields.Str(required=True)  # This field is required and checks if is String.


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
