from flask import Blueprint
from .auth_routes import auth_bp
from .admin_routes import admin_bp
from .user_routes import user_bp


def register_api_routes(app):

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(user_bp, url_prefix="/api/user")

    # Public endpoint for testt
    @app.route("/")
    def index():
        return "This is a public endpoint."
