#!/usr/bin/python3

"""
User REST API Module

This module provides CRUD endpoints for managing Users

Endpoints:
    - GET /users: Retrieve a list of all users.
    - POST /users: Create a new user
    - GET /users/<user_id>/: Get a specific user by ID
    - GET /users/<user_id>/orders: Retrieve all orders made by from a user by ID.
    - GET /users/<user_id>/orders: Create a new order for this user
    - GET /users/<user_id>/orders/<order_id>: Retrieve a specific order by ID from a specific user by ID.
    - PUT /order/<id>: Update an existing order by ID.
    - DELETE /order/<id>: Delete a order by ID.
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User
from models.order import Order
from models.measurements import Measurements


@app_views.route("/users")
@app_views.route("/users/<user_id>")
def get_users(user_id=None):
    """get a list of all users in storage or
       get a specific user by ID
    """

    if user_id is None:
        return make_response(jsonify([
            user.to_dict() for user in storage.all(User).values()
        ]))
    
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route("/users", methods=["POST"])
def create_user(user_id=None):
    """create a new user
    """
    user_data = request.get_json(silent=True)
    if user_data is None:
        abort(400, "Not a JSON")

    if "email" not in user_data:
        abort(400, "Missing email")
    if "password" not in user_data:
        abort(400, "Missing password")
    user = User(email=user_data["email"], password=user_data["password"])
    ignore_attr = ["email", "password"]
    [
        setattr(user, key, user_data[key])
        for key in user_data
        if key not in ignore_attr
    ]

    user.save()
    return make_response(jsonify(user.to_dict()), 201)




@app_views.route("/users/<user_id>/orders")
@app_views.route("/users/<user_id>/orders/<order_id>")
def get_user_orders(user_id=None, order_id=None):
    """get a list of all orders made by a user
       or get a specific order from a user
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    orders = storage.all(Order).values()

    if order_id is None:
        return make_response(jsonify([
            order.to_dict() for order in orders
            if order.user_id == user_id
        ]), 200)
    
    order = storage.get(Order, order_id)
    if order is None or order.user_id != user.id:
        abort(404)

    return make_response(jsonify(order.to_dict()), 200)
    

    

@app_views.route("/users/<user_id>/orders", methods=["POST"])
def create_user_orders(user_id=None, order_id=None):
    """create a new order for this user
    """
    user = storage.get(User, user_id)
    if user is None:
        abort()

    order_data = request.get_json(silent=True)
    if order_data is None:
        abort(400, "Not a JSON")

    if "product_id" not in order_data:
        abort(400, "Missing product_id")
    if "measurements" not in order_data:
        abort(400, "Missing measurements")

    new_order = Order(product_id=order_data['product_id'],
                      user_id = user_id)

    
    new_order.measurements = Measurements()
    [
        setattr(new_order.measurements, measurement, value)
        for measurement, value in order_data["measurements"].items()
    ]

    new_order.save()
    return make_response(jsonify(new_order.to_dict()), 200)