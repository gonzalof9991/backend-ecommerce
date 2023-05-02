import os
import requests
from flask import Flask, request, jsonify
from flask_smorest import Api
# Import routes
from routes.azure import blp as AzureBlueprint
from routes.product import blp as ProductBlueprint
from routes.category import blp as CategoryBlueprint
from routes.user import blp as UserBlueprint
from routes.wallet import blp as WalletBlueprint
from routes.order import blp as OrderBlueprint
# Importamos env
from dotenv import load_dotenv
# Import BD
from connections.db import db
from flask_migrate import Migrate
import models


def create_app(db_url=None):
    app = Flask(__name__)
    # Cargar .env
    load_dotenv()
    # Configuración de Flask
    app.config["API_TITLE"] = "E-Commerce REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # Configuración DB
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['SECRET_KEY'] = 'secret!'
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    # crear todas las tablas de la bd antes de la consulta
    @app.before_first_request
    def create_tables():
        db.create_all()

    # Register blueprints
    api.register_blueprint(AzureBlueprint)
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(OrderBlueprint)
    api.register_blueprint(WalletBlueprint)

    @app.route('/api/v1/query')
    def query_example():
        data = request.json
        print(data['total'])
        # obtener una instancia de la sesión de la base de datos
        session = db.session
        # ejecutar una consulta nativa
        results = session.execute("""
            SELECT 
                u.name AS "Nombre",
                SUM(o.total) AS "Suma"
            FROM public."user" as u
            JOIN public."order" as o
            ON u.id = o.user_id
            GROUP BY u.name
            HAVING SUM(o.total) >= """ + str(data['total']) + """;
        """)
        # obtener los resultados de la consulta
        rows = results.fetchall()
        data = []
        # procesar los resultados
        for row in rows:
            # hacer algo con cada fila
            print(row)
            item = {'name': row[0], 'amount': row[1]}
            data.append(item)
        # devolver los resultados
        return jsonify(data)

    return app
