from functools import wraps
from flask import session, jsonify, g

from app import db
from app.models.user import User


def login_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):

        # Check whether a user ID exists in the session
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({
                "error": "Authentication required. Please log in."
            }), 401

        # Find the user in the database
        user = db.session.get(User, user_id)

        if user is None:
            session.clear()
            return jsonify({
                "error": "User not found. Please log in again."
            }), 401

        # Make the logged-in user available to the route
        g.current_user = user

        return route_function(*args, **kwargs)

    return decorated_function

