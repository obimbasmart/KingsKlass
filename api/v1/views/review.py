#!/usr/bin/python3

"""
Review REST API Module

This module provides CRUD endpoints for managing Product Reviews

Endpoints:
    - POST  | GET /products/<product_id>/reviews: 
            Retrieve a list of all review of a product
            Create a new review 
            
    - GET|POST|UPDATE /reviews/<review_id>:  review by id
    - GET /reviews : get a list of all reviews
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.product import Product
from models.review import Review
from models.user import User

@app_views.route("/products/<product_id>/reviews", methods=["GET", "POST"])
def get_product_review(product_id=None):
    """Retrieves a list of all Review of a product or
       Create a new review for a product"""
    product = storage.get(Product, product_id)

    if product is None:
        abort(404)

    if request.method == "GET":
        return (jsonify([review.to_dict()
                         for review in product.reviews]), 200)
    
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    if "user_id" not in data:
        abort("Missing user_id")

    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)

    if "comment" not in data:
        abort(400, "Missing comment")
    if "rating" not in data:
        abort(400, "Missing rating")

    review = Review(user_id = data["user_id"],
                    product_id = product_id,
                    comment = data["comment"],
                    rating=data["rating"])

    review.save()
    return (jsonify(review.to_dict()), 200)


@app_views.route("/reviews", methods=["GET"])
@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"])
def get_review(review_id=None):
    """Get all reviews or Retrieves a Review object by ID"""

    if review_id is None:
        return (jsonify(
            [
                review.to_dict()
                for review in storage.all(Review).values()
            ]
        ))
    
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == "GET":
        return jsonify(review.to_dict()), 200
    
    if request.method == "DELETE":
        review.delete()
        storage.save()
        return jsonify({}), 200
    
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    if "comment" not in data:
        abort(400, "Missing comment")
    if "rating" not in data:
        abort(400, "Missing rating")

    review.comment = data["comment"]
    review.rating = data["rating"]

    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>/product")
def get_review_product(review_id=None):
    """Get the product for a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.product.to_dict()), 200
