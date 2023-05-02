
import requests
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from connections.db import db
from request.schemas import AzureFileSchema
from services.blob import BlobService 
blp = Blueprint("Azure", "azure", description="Operations on Azure")

@blp.route("/azure/upload/")
class AzureFile(MethodView):
    @blp.arguments(AzureFileSchema)
    def post(self, azure_data):
        try:
            container = 'testcontenedor'
            #filename = request.args.get('filename')
            data = request.files['file']
            filename = data.filename
            print(filename)
            blob_service = BlobService()
            return blob_service.upload_blob(filename=filename, container=container, data=data)
        except ValueError as e:
            abort(400, message=str(e))
        except ConnectionError as e:
            abort(400, message=str(e))

