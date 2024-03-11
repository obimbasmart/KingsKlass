#!/usr/bin/python3
"""module for REST API entry point"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from api.v1.auth import auth_blueprint
from os import getenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Set default expiration to 1 hour
# CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
CORS(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "c179e3d-3629-4071-8cb7-77e30c8cd697"  # Change this!
jwt = JWTManager(app)


@app.errorhandler(404)
def resource_not_found(self):
    """handle 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_connection(self):
    """close database storage session"""
    storage.close()

@app.teardown_request
def session_clear(exception=None):
    """rollback DB session on rollback error Exception"""
    storage.close()
    if exception and storage.__Session.is_active:
        storage.__Session.rollback()

app.register_blueprint(app_views)
app.register_blueprint(auth_blueprint)


if __name__ == "__main__":
    api_host = getenv("KS_API_HOST", "0.0.0.0")
    api_port = getenv("KS_API_PORT", 5000)
    app.run(host=api_host, port=api_port, threaded=True)
