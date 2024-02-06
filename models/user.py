#!/usr/bin/python

"""User Module

This module defines the User class, representing signed in users.

Attributes:
    - first_name (str): User first name.
    - last_name (float): User last name.
    - email (str): User email address.
    - password (str): User password
    - phone_no (str) : User phone number
    - is_admin (boolean) : specifies if user is an admin or just regular user
"""

from hashlib import md5
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, Integer, Boolean


class User(BaseModel, Base):
    """User class """

    __tablename__ = 'users'
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    email = Column(String(1024), nullable=False)
    password = Column(String(1024), nullable=False)
    phone_no = Column(String(128), nullable=True)
    is_admin = Column(Boolean, unique=False, default=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        if name == 'password':
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)