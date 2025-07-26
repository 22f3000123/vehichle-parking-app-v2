from flask import Flask
from .extensions import db, security
from flask_cors import CORS
from .models import User, Role
from flask_security import SQLAlchemyUserDatastore
from .api.routes import register_api_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    CORS(
        app,
        origins=["http://localhost:5173", "http://127.0.0.1:5173", "localhost:5173"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"]
    )

    db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    register_api_routes(app)

    return app
