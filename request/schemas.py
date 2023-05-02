from marshmallow import Schema, fields


class AzureFileSchema(Schema):
    filename = fields.Str(required=False)
    container = fields.Str(required=False)
    data = fields.Str(required=False)


class PlainCategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    status = fields.Boolean(required=False)


class CategorySchema(PlainCategorySchema):
    products = fields.List(fields.Nested('PlainProductSchema'), dump_only=True)


class PlainProductSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    price = fields.Float(required=False)
    stock = fields.Integer(required=False)
    status = fields.Boolean(required=False)
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)



class ProductSchema(PlainProductSchema):
    category_id = fields.Integer(required=True, load_only=True)
    category = fields.Nested('PlainCategorySchema', dump_only=True)
    orders = fields.List(fields.Nested('PlainOrderSchema'), dump_only=True)


class PlainWalletSchema(Schema):
    id = fields.Integer(dump_only=True)
    balance = fields.Float(required=False)
    status = fields.Boolean(required=False)
    is_active = fields.Boolean(required=False)


class WalletSchema(PlainWalletSchema):
    user_id = fields.Integer(required=True, load_only=True)
    user = fields.Nested('PlainUserSchema', dump_only=True)


class PlainUserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)
    # Nunca se debe devolver la contraseña del usuario cuando se devuelve una información
    password = fields.Str(required=True, load_only=True)
    email = fields.Str(required=True)
    name = fields.Str(required=True)
    status = fields.Boolean(required=False)
    is_active = fields.Boolean(required=False)


class UserSchema(PlainUserSchema):
    orders = fields.List(fields.Nested("PlainOrderSchema"), dump_only=True)
    wallet = fields.Nested("PlainWalletSchema", dump_only=True)


class PlainOrderSchema(Schema):
    id = fields.Integer(dump_only=True)
    code = fields.Str(required=False)
    description = fields.Str(required=False)
    status = fields.Boolean(required=False)
    total = fields.Float(required=False)
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)


class OrderSchema(PlainOrderSchema):
    user_id = fields.Integer(required=False, load_only=True)
    user = fields.Nested('PlainUserSchema', dump_only=True)
    products = fields.List(fields.Nested('PlainProductSchema'), dump_only=True)
    product_items = fields.List(fields.Nested('ProductItemSchema'),  required=True)


class ProductItemSchema(Schema):
    id = fields.Integer(required=True)
    quantity = fields.Integer(required=False)


class ProductAndOrderSchema(Schema):
    message = fields.Str()
    product = fields.Nested(ProductSchema)
    order = fields.Nested(OrderSchema)
