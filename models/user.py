#!/usr/bin/python

"""User Module

This module defines the User class, representing signed in users.

Attributes:
    - first_name (str): User first name.
    - last_name (float): User last name.
    - email (str): User email address.
    - username(str): User username
    - password (str): User password
    - phone_no (str) : User phone number
    - is_admin (boolean) : specifies if user is an admin or just regular user
"""

from hashlib import md5
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Boolean
from models.json_dict import JsonEncodedDict, default_measurement


class User(BaseModel, Base):
    """User class """

    __tablename__ = 'users'
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    username = Column(String(128), nullable=False)
    email = Column(String(1024), nullable=False)
    password = Column(String(1024), nullable=False)
    phone_no = Column(String(128), nullable=True)
    is_admin = Column(Boolean, unique=False, default=False)
    measurements = Column(JsonEncodedDict, default=default_measurement)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        if name == 'password':
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)


    def to_dict(self):
        user_dict = super().to_dict()
        del user_dict["measurements"]
        return user_dict