
from flask import Blueprint, request, jsonify, session
from marshmallow import ValidationError

from app import db
from app.models.user import User
from app.schemas.user_schema import user_schema
from app.auth.decorators import login_required


auth_bp = Blueprint("auth", __name__, url_prefix="/api")


# REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    try:
        validated_data = user_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    # Check whether email already exists
    existing_user = User.query.filter_by(
        email=validated_data["email"]
    ).first()

    if existing_user:
        return jsonify({
            "error": "Email is already registered"
        }), 409

    # Create user
    new_user = User(
        username=validated_data["username"],
        email=validated_data["email"]
    )

    # Hash password before saving
    new_user.set_password(validated_data["password"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": user_schema.dump(new_user)
    }), 201


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    # Find user by email
    user = User.query.filter_by(email=email).first()

    # Verify password
    if user is None or not user.check_password(password):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    # Clear any previous session
    session.clear()

    # Store logged-in user's ID
    session["user_id"] = user.id

    return jsonify({
        "message": "Login successful",
        "user": user_schema.dump(user)
    }), 200


# CURRENT USER
@auth_bp.route("/me", methods=["GET"])
def get_current_user():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Authentication required"
        }), 401

    user = db.session.get(User, user_id)

    if user is None:
        session.clear()
        return jsonify({
            "error": "User not found"
        }), 401

    return jsonify({
        "user": user_schema.dump(user)
    }), 200


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()

    return jsonify({
        "message": "Logout successful"
    }), 200

