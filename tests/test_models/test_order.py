#!/usr/bin/python3

"""
    Order Test Module

    This module contains unit tests for the Order-related functionalities.

    The tests cover various aspects such as Order creation, modification, and validation.
"""

import unittest
from models import storage
from models.user import User
from tests.test_models.test_base_model import TestBaseModel
from models.product import Product
from models.order import Order
import json

class TestOrder(unittest.TestCase):

    product = None
    user = None
    order = None

    def setUp(self):
        """---create a new order"""
        self.user = User(email="test_123@gmail.com", password="abcde")
        self.product = Product(name='Jocos', price=1234.56,
                     img_url='bbb.png', estimated=4, description="Nice senator")
        
        self.user.save()
        self.product.save()

        self.order = Order(product_id=self.product.id, user_id=self.user.id)
        print(self.order.measurements)
        self.order.save()
        
    def test_base_attrs(self):
        """---test that Order inherits from BaseModel and has all required base attrs"""
        TestBaseModel.check_base_attributes(self, self.order)


        order_from_storage = storage.get(Order, self.order.id)
        self.assertEqual(order_from_storage.order_status, 'PENDING')
        self.assertEqual(order_from_storage.order_progress, 'AWAITING_COMFIRMATION')

    def test_save(self):
        """"---save: persist object to db storage"""
        order = Order(product_id=self.product.id, user_id=self.user.id)
        n_order_inital = len(storage.all(Order))

        # before saving
        self.assertEqual(storage.get(Order, order.id), None)
        self.assertEqual(len(storage.all(Order)), n_order_inital)

        # after saving
        order.save()
        n_order = len(storage.all(Order))
        self.assertNotEqual(None, storage.get(Order, order.id))
        self.assertNotEqual(n_order, n_order_inital)

    def test_delete(self):
        """---delete the current instance from the storage"""

        self.assertNotEqual(None, storage.get(Order, self.order.id))
        self.order.delete()
        self.assertEqual(None, storage.get(Order, self.order.id))

    def test_to_dict(self):
        """---returns a dictionary containing all keys/values of the instance"""
        self.assertIsInstance(self.order.to_dict(), dict)

    def test_order_measurement(self):
        """--- test that order.measurements returns a dict of measurments"""
        self.assertIsInstance(self.order.measurements, dict)
    

