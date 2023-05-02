
import os

from dotenv import load_dotenv

load_dotenv()


class BlobService:
   

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    if connection_string is None:
        raise ValueError("Azure Storage connection string is missing")

    def upload_blob(self, filename: str, container: str, data: bytes):
        from azure.storage.blob import BlobServiceClient
        try:
            blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            blob_client = blob_service_client.get_blob_client(container=container, blob=filename)
            blob_client.upload_blob(data)
            return {"message": "File uploaded successfully"}, 201
        except ValueError as e:
            return e
        except ConnectionError  as e:
            return e



# upload method to Blob Storag