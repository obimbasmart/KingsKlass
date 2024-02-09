#!/usr/bin/python3

from hashlib import md5
from flask import jsonify, request, abort
from flask_jwt_extended import create_access_token
from api.v1.auth import auth_blueprint
from models import storage

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.


@auth_blueprint.route("/login", methods=["POST"])
def login():
    """handle user login authentication"""

    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, "Not a JSON")

    email = user_data.get("email", None)
    password = user_data.get("password", None)
    user = storage.get_user(email)

    if user is None or user.password != md5(password.encode()).hexdigest():
        return jsonify({"error": "Incorrect email or password"}), 401

    claims = {"is_admin": user.is_admin}
    access_token = create_access_token(
        identity=user.id, additional_claims=claims)
    return jsonify(access_token=access_token)
