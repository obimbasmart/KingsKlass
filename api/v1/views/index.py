#!/usr/bin/python3
"""index default view"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def get_status():
    """get api status"""
    return jsonify({"status": "OK"})


# @app_views.route("/stats")
# def object_stats():
#     pass