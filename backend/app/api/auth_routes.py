from flask import Blueprint, request, jsonify
from flask_security import (
    hash_password,
    verify_password,
    login_user,
    logout_user,
    current_user,
)
from ..models import db, User
import re

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([first_name, last_name, username, email, password]):
        return jsonify({"message": "All fields are required"}), 400

    if not re.match(r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$", email):
        return jsonify({"message": "Invalid email format"}), 400

    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters long"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User with this email already exists"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User with this username already exists"}), 400

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        password=hash_password(password),
        active=True,
        fs_uniquifier=email,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not verify_password(password, user.password):
        return jsonify({"message": "Invalid credentials"}), 401

    login_user(user)

    return (
        jsonify(
            {
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "roles": [role.name for role in user.roles],
                },
            }
        ),
        200,
    )


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    if current_user.is_authenticated:
        return (
            jsonify(
                {
                    "id": current_user.id,
                    "name": f"{current_user.first_name} {current_user.last_name}",
                    "username": current_user.username,
                    "email": current_user.email,
                    "roles": [role.name for role in current_user.roles],
                }
            ),
            200,
        )
    return jsonify({"message": "Not authenticated"}), 401
