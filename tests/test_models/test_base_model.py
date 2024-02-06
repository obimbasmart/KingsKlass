#!/usr/bin/python3

"""Unit test for BaseModel class"""

from datetime import datetime
import os
import unittest
from models.base_model import BaseModel
from models.user import User
import MySQLdb

class TestBaseModel(unittest.TestCase):
    """Test BaseModel"""

    def test_base_attrs(self):
        """--- test base attrs"""
        m1 = BaseModel()
        self.check_base_attributes(m1)

    def test_to_dict(self):
        """---test to_dict method"""
        m1 = BaseModel()
        self.assertIs(type(m1.to_dict()), dict)
        self.assertIn('updated_at', m1.to_dict())
        self.assertIn('created_at', m1.to_dict())

    def check_base_attributes(self, obj):
        self.assertIsInstance(obj, BaseModel)
        self.assertIs(type(obj.id), str)
        self.assertIs(type(obj.updated_at), datetime)
        self.assertIs(type(obj.created_at), datetime)


        