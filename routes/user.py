import requests
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from connections.db import db
from models import UserModel
from request.schemas import UserSchema
from passlib.hash import pbkdf2_sha256
from sqlalchemy import or_

blp = Blueprint("User", "user", description="Operations on User")


@blp.route("/api/v1/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        try:
            # return Users
            users = UserModel.query.all()
            return users
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        try:
            if UserModel.query.filter(
                    or_(UserModel.username == user_data["username"], UserModel.email == user_data["email"])).first():
                abort(409, message="A user with that username already exists.")

            user = UserModel(
                username=user_data["username"],
                email=user_data["email"],
                password=pbkdf2_sha256.hash(user_data["password"]),
                name=user_data["name"],
                is_active=user_data["is_active"],
                status=user_data["status"],
            )
            db.session.add(user)
            db.session.commit()
            return user
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))


# create class User
@blp.route("/api/v1/user/<int:id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, id):
        try:
            user = UserModel.query.filter_by(id=id).first()
            return user
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

    # Update User
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, id):
        try:
            user = UserModel.query.filter_by(id=id).first()
            if user is None:
                abort(404, message="User not found")
            user.username = user_data["username"]
            user.email = user_data["email"]
            user.password = pbkdf2_sha256.hash(user_data["password"])
            user.name = user_data["name"]
            user.is_active = user_data["is_active"]
            user.status = user_data["status"]
            db.session.commit()
            return user
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))
