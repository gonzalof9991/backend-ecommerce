import requests
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from connections.db import db
from models import ProductModel
from request.schemas import ProductSchema

blp = Blueprint("Product", "product", description="Operations on Product")


@blp.route("/api/v1/product")
class ProductList(MethodView):
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        try:
            # return Products
            products = ProductModel.query.all()
            return products
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        try:
            product = ProductModel(**product_data)
            db.session.add(product)
            db.session.commit()
            return product
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))


# Create class Product
@blp.route("/api/v1/product/<int:id>")
class Order(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, id):
        try:
            product = ProductModel.query.filter_by(id=id).first()
            return product
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

    # Update Order
    @blp.arguments(ProductSchema)
    @blp.response(200, ProductSchema)
    def put(self, order_data, id):
        try:
            product = ProductModel.query.filter_by(id=id).first()
            product.name = order_data['name']
            product.price = order_data['price']
            product.description = order_data['description']
            product.stock = order_data['stock']
            product.save_to_db()
            return product
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

    # Delete Order
    @blp.response(200, ProductSchema)
    def delete(self, id):
        try:
            product = ProductModel.query.filter_by(id=id).first()
            product.delete_to_db()
            return product
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))
