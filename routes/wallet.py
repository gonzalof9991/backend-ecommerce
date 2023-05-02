import requests
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from connections.db import db
from models import WalletModel
from request.schemas import WalletSchema
from sqlalchemy import or_

blp = Blueprint("Wallet", "wallet", description="Operations on Wallet")


@blp.route("/api/v1/wallet")
class UserList(MethodView):
    @blp.response(200, WalletSchema(many=True))
    def get(self):
        try:
            # return Users
            wallets = WalletModel.query.all()
            return wallets
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

    @blp.arguments(WalletSchema)
    @blp.response(201, WalletSchema)
    def post(self, wallet_data):
        try:

            wallet = WalletModel(
                user_id=wallet_data["user_id"],
                balance=wallet_data["balance"],
                status=wallet_data["status"],
                is_active=wallet_data["is_active"],
            )
            wallet.save_to_db()
            return wallet
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))


# create class Wallet
@blp.route("/api/v1/wallet/<int:id>")
class Wallet(MethodView):
    @blp.response(200, WalletSchema)
    def get(self, id):
        try:
            wallet = WalletModel.query.filter_by(id=id).first()
            return wallet
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

    # Update Wallet
    @blp.arguments(WalletSchema)
    @blp.response(200, WalletSchema)
    def put(self, wallet_data, id):
        try:
            wallet = WalletModel.query.filter_by(id=id).first()
            wallet.user_id = wallet_data['user_id']
            wallet.balance = wallet_data['balance']
            wallet.status = wallet_data['status']
            wallet.is_active = wallet_data['is_active']
            wallet.save_to_db()
            return wallet
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))