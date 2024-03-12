#!/usr/bin/python3

"""
    User Test Module

    This module contains unit tests for the signed in user related functionalities.
"""

from models import storage
from datetime import datetime
import unittest
from models.user import User
from tests.test_models.test_base_model import TestBaseModel

class TestUser(unittest.TestCase):

    user = None

    def setUp(self):
        self.user = User(email=f"test_{datetime.now().microsecond}@gmail.com",
                         username="Okonja", password="abcde")
        self.user.save()
    
    def test_base_attrs(self):
        """---test that User inherits from BaseModel and has all required base attrs"""
        TestBaseModel.check_base_attributes(self, self.user)

    def test_save(self):
        """---save: persist object to db storage"""

        n_User_inital = len(storage.all(User))

        u = User(email=f"test_{datetime.now().microsecond}@gmail.com",
                 username="Ikenga", password="abcde")
        u.description = "E good"

        # before saving
        self.assertEqual(storage.get(User, u.id), None)
        self.assertEqual(len(storage.all(User)), n_User_inital)

        # after saving
        u.save()
        n_User = len(storage.all(User))
        self.assertNotEqual(None, storage.get(User, u.id))
        self.assertNotEqual(n_User, n_User_inital)

    def test_delete(self):
        """---delete the current instance from the storage"""
        self.assertNotEqual(None, storage.get(User, self.user.id))

        self.user.delete()
        storage.save()
        self.assertEqual(None, storage.get(User, self.user.id))

    def test_to_dict(self):
        """---returns a dictionary containing all keys/values of the instance"""
        self.assertIsInstance(self.user.to_dict(), dict)
        self.assertNotIn('password', self.user.to_dict())

    def test_order_measurement(self):
        """--- test that user.measurements returns a dict of measurments"""
        self.assertIsInstance(self.user.measurements, dict)
        self.assertNotEqual(self.user.measurements, {})