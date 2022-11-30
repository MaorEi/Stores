from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)  # We only want to use it for returning data from the client.
    name = fields.Str(required=True)  # This field is required both ends (getting & returning) and checks if is String.
    price = fields.Float(required=True)  # This field is required and checks if is Float.


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)  # We only want to use it for getting data from the client.
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    # store = fields.Nested(lambda: StoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    # We use PlainItemSchema (and PlainStoreSchema) in order to avoid infinite nesting recursion.
    # items = fields.List(fields.Nested(lambda: ItemSchema()), dump_only=True)
    # When we want to use a Schema that hasn't been defined yet, we use lambda.
