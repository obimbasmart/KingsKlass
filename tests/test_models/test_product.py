#!/usr/bin/python3

"""
    Product Test Module

    This module contains unit tests for the product-related functionalities.

    The tests cover various aspects such as product creation, modification, and validation.
"""

from datetime import datetime
import unittest
from models import storage
from models.base_model import BaseModel
from models.review import Review
from models.user import User
from models.category import Category
from tests.test_models.test_base_model import TestBaseModel
from models.product import Product


class TestProduct(unittest.TestCase):

    product = None

    def setUp(self):
        """setup for each test"""
        self.product = Product(name='KofuCap 4rm test',
                               price=134.56,
                               img_url='test_2.png', estimated=4,
                               description="Good dress")
        self.product.save()

    def test_base_attrs(self):
        """---test that Product inherits from BaseModel and has all required base attrs"""
        TestBaseModel.check_base_attributes(self, self.product)

    def test_save(self):
        """---save: persist object to db storage"""

        n_product_inital = len(storage.all(Product))

        p1 = Product(name='Senator', price=1234.56,
                     img_url='bbb.png', estimated=4)
        p1.description = "E good"

        # before saving
        self.assertEqual(storage.get(Product, p1.id), None)
        self.assertEqual(len(storage.all(Product)), n_product_inital)

        # after saving
        p1.save()
        n_product = len(storage.all(Product))
        self.assertNotEqual(None, storage.get(Product, p1.id))
        self.assertNotEqual(n_product, n_product_inital)

    def test_delete(self):
        """---delete the current instance from the storage"""
        self.assertNotEqual(None, storage.get(Product, self.product.id))
        self.product.delete()
        self.assertEqual(None, storage.get(Product, self.product.id))

    def test_to_dict(self):
        """---returns a dictionary containing all keys/values of the instance"""
        self.assertIsInstance(self.product.to_dict(), dict)
        self.assertIn("name", self.product.to_dict())
        self.assertIn("price", self.product.to_dict())
        self.assertIn("description", self.product.to_dict())
        self.assertIn("img_url", self.product.to_dict())
        self.assertIn("estimated", self.product.to_dict())
        self.assertIn("on_draft", self.product.to_dict())

    def test_review_relationship(self):
        """---check if product.reviews returns a list of reviews"""

        u1 = User(email="test_1@gmail.com", password="my_pwd")
        r1 = Review(product_id=self.product.id, user_id=u1.id,
                    comment="Good clothe", rating=4)
        u1.save()
        r1.save()
        product_from_storage = storage.get(Product, self.product.id)
        self.assertIsInstance(product_from_storage.reviews, list)
        self.assertIsInstance(product_from_storage.reviews[0], Review)

    def test_category_relationship(self):
        """---check if product.categories return a list of categories"""
        c1 = Category(id="Chinos")
        self.product.categories.append(c1)

        c1.save()
        cc = storage.get(Category, c1.id)
        self.assertIsInstance(self.product.categories, list)
        self.assertIsInstance(self.product.categories[0], Category)
