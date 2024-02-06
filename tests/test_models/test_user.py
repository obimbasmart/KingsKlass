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

    def test_base_attrs(self):
        """---test that User inherits from BaseModel and has all required base attrs"""
        TestBaseModel.check_base_attributes(self, User())

    def test_save(self):
        """---save: persist object to db storage"""

        n_User_inital = len(storage.all(User))

        u = u = User(email=f"test_{datetime.now().microsecond}@gmail.com", password="abcd")
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
        u = User(email="test@gmail.com", password="abcd")
        u.save()

        self.assertNotEqual(None, storage.get(User, u.id))
        u.delete()
        self.assertEqual(None, storage.get(User, u.id))

    def test_to_dict(self):
        """---returns a dictionary containing all keys/values of the instance"""
        u = User(email=f"test_{datetime.now().microsecond}@gmail.com", password="abcd")

        self.assertIsInstance(u.to_dict(), dict)
        self.assertNotIn('password', u.to_dict())