
import requests
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from connections.db import db
from models import CategoryModel
from request.schemas import CategorySchema
blp = Blueprint("Category", "category", description="Operations on Category")

@blp.route("/api/v1/category")
class CategoryList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        try:
            # return Categories
            categories = CategoryModel.query.all()
            return categories
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        try:
            category = CategoryModel(**category_data)
            db.session.add(category)
            db.session.commit()
            return category
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

