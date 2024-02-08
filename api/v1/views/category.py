#!/usr/bin/python3

"""
Category REST API Module

This module provides CRUD endpoints for managing Product Categories

Endpoints:
    - GET /categories: Retrieve a list of all categories.
    - POST /categories: Create a new category
    - GET /category/<category_id>/products: Get a list of products belonging to this category
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.category import Category
from exceptions.validation_exceptions import NonUniqueValueError

@app_views.route("/categories", methods=["GET"])
def get_categories():
    """get a list of all Unique categories"""
    categories = storage.all(Category).values()
    return jsonify([
        category.id for category in categories
    ])


@app_views.route("/categories/<category_name>", methods=["POST", "DELETE", "PUT"])
def get_create_category(category_name=None):
    """create or delete a category"""

    if category_name is None:
        abort(404)

    if request.method == "POST":
        try:
            new_category = Category(id=category_name)
            new_category.save()
        except NonUniqueValueError as err:
            abort(400, err)
        return jsonify(new_category.to_dict()), 200

    category = storage.get(Category, category_name)
    if category is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(category)
        storage.save()
        return jsonify({}), 200
    
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    if "name" not in data:
        abort(400, "Missing name")

    category.id = data['name']
    category.save()

    return jsonify(category.to_dict()), 200    


    
@app_views.route("/categories/<category_name>/products")
def get_product_by_category(category_name):
    """get a list of products by category_name"""
    category = storage.get(Category, category_name)

    if category is None:
        abort(404)

    return jsonify([
        product.to_dict()
        for product in category.products
    ])