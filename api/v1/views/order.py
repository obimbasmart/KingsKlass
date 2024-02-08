#!/usr/bin/python3

"""
Order REST API Module

This module provides CRUD endpoints for managing Orders

Endpoints:
    - GET /orders: Retrieve a list of all orders.
    - GET /orders/<status>/: Get a list of all otheres of status
    - GET /order/<id>: Retrieve details of a specific order by ID.
    - PUT /order/<id>: Update an existing order by ID.
    - DELETE /order/<id>: Delete a order by ID.
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.order import Order


@app_views.route("/orders")
@app_views.route("/orders/<order_id>")
def get_post_order(order_id=None):
    """get a list of all orders in storage or"""
    
    if order_id is None:
        return make_response(jsonify([
            order.to_dict() for order in storage.all(Order).values()
        ]))

    order = storage.get(Order, order_id)
    if order is None:
        abort(404)
    return make_response(jsonify(order.to_dict()), 200)


@app_views.route("/orders/<order_id>/measurements")
def get_order_measurements(order_id=None):
    """get a list of all measurement for this order"""
    order = storage.get(Order, order_id)
    if order is None:
        abort(404)

    return jsonify(order.measurements)
    

    
    

    