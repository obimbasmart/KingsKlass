#!/usr/bin/python3

"""
Product REST API Module

This module provides CRUD endpoints for managing products in a RESTful manner

Endpoints:
    - GET /products: Retrieve a list of all products.
    - GET /products/<id>: Retrieve details of a specific product by ID.
    - POST /products: Create a new product.
    - PUT /products/<id>: Update an existing product by ID.
    - DELETE /products/<id>: Delete a product by ID.
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.product import Product
from models.category import Category
from flask_jwt_extended import jwt_required
from api.v1.auth.admin import admin_required

@app_views.route("/products")
def get_product():
    """get a list of all products in storage or
       create a new  product """
    products = storage.all(Product).values()
    return make_response(jsonify([
        product.to_dict()
        for product in products]), 200)


@app_views.route("/products", methods=["POST"])
@admin_required()
def post_product():
    """post a new product"""
    product_data = request.get_json(silent=True)
    if product_data is None:
        abort(400, "Not a JSON")

    if "name" not in product_data:
        abort(400, "Missing name")
    if "price" not in product_data:
        abort(400, "Missing price")
    if "description" not in product_data:
        abort(400, "Missing description")
    if "estimated" not in product_data:
        abort(400, "Missing estimated")
    if "img_url" not in product_data:
        abort(400, "Missing img_url")
    if "categories" not in product_data:
        abort(400, "Missing categories")

    new_product = Product(name = product_data['name'],
                          price = product_data['price'],
                          description = product_data['description'],
                          estimated = product_data['estimated'],
                          img_url = product_data['img_url'])
    
    for id in product_data.get("categories"):
        category = storage.get(Category, id)
        if category is not None:
            new_product.categories.append(category)

        
    new_product.save()
    return make_response(jsonify(new_product.to_dict()), 201)

@app_views.route("/products/<product_id>", methods=["GET", "PUT"])
def get_update_product(product_id):
    """get or update a product"""

    product = storage.get(Product, product_id)
    if product is None:
        abort(404)

    if request.method == "GET":
        return make_response(jsonify(product.to_dict()), 200)
    
    product_data = request.get_json(silent=True)
    if product_data is None:
        abort(400, "Not a JSON")

    ignore_attr = ["id", "updated_at", "created_at", "state_id"]
    [
        setattr(product, attr, product_data[attr])
        for attr in product_data
        if attr not in ignore_attr
    ]

    product.save()
    return make_response(jsonify(product.to_dict()), 200)

@app_views.route("/products/categories/<category_id>")
def get_products_by_category(category_id=None):
    """get all products by a category"""
    category = storage.get(Category, category_id)

    if category is None:
        abort(404)

    return jsonify([prod.to_dict() for prod in category.products])
    

@app_views.route("/products/<product_id>", methods=["DELETE"])
@admin_required()
def delete_update_product(product_id):
    """delete a product from storage"""
    product = storage.get(Product, product_id)
    if product is None:
        abort(404)

    product.delete()
    storage.save()
    return jsonify({}), 200


