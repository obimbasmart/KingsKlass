#!/usr/bin/python3
"""initialize authentication blueprint"""

from flask import Blueprint

auth_blueprint = Blueprint("app_blueprint", __name__)

from . import user
from . import admin