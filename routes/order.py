import requests
import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from connections.db import db
from models import OrderModel, ProductModel
from request.schemas import OrderSchema
from services.order import OrderService

blp = Blueprint("Order", "order", description="Operations on Order")

order_service = OrderService()

@blp.route("/api/v1/order")
class OrderList(MethodView):
    @blp.response(200, OrderSchema(many=True))
    def get(self):
        try:
            # return orders filter by deleted_at null
            orders = OrderModel.query.filter_by(deleted_at=None).all()
            return orders
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

    @blp.arguments(OrderSchema)
    @blp.response(201, OrderSchema)
    def post(self, order_data):
        try:
            products = order_service.insert_product(order_data['product_items'])
            total = order_service.calculate_total(order_data['product_items'])
            code = order_service.generate_code()
            # restart amount a Wallet
            order_service.restart_amount(order_data['user_id'], total)
            order = OrderModel(
                user_id=order_data['user_id'],
                products=products,
                total=total,
                code=code
            )
            # Save Order
            order.save_to_db()
            return order

        except ValueError as e:
            abort(400, message=str(e))

        except ConnectionError as e:
            abort(400, message=str(e))


# Create class Order
@blp.route("/api/v1/order/<int:id>")
class Order(MethodView):

    # Get Order
    @blp.response(200, OrderSchema)
    def get(self, id):
        try:
            order = OrderModel.query.filter_by(id=id).first()
            return order
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

    # Update Order
    @blp.arguments(OrderSchema)
    @blp.response(200, OrderSchema)
    def put(self, order_data, id):
        try:
            order = OrderModel.query.filter_by(id=id).first()
            order.user_id = order_data['user_id']
            order.products = order_service.insert_product(order_data['products_id'])
            order.total = order_service.calculate_total(order_data['products_id'])
            # order.code = OrderService.generate_code()
            order.save_to_db()
            return order
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

    # Delete Order
    @blp.response(200, OrderSchema)
    def delete(self, id):
        try:
            order = OrderModel.query.filter_by(id=id).first()
            order.delete_from_db()
            return order
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))
