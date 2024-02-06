#!/usr/bin/python3

"""
    Review Test Module

    This module contains unit tests for the review-related functionalities.
"""

import unittest
from models import storage
from models.user import User
from tests.test_models.test_base_model import TestBaseModel
from models.product import Product
from models.review import Review
from models.measurement import Measurement

class TestReview(unittest.TestCase):

    product = None
    user = None
    review = None

    def setUp(self):
        """---create a new review"""
        self.user = User(email="test_123@gmail.com", password="abcde")
        self.product = Product(name='Jocos', price=1234.56,
                     img_url='bbb.png', estimated=4, description="Nice senator")
        
        self.user.save()
        self.product.save()

        self.review = Review(product_id=self.product.id, user_id=self.user.id)
        self.review.comment = "KingsKlass is a Nice place to do my clothes"
        self.review.rating = 3

        self.review.save()
        
    def test_base_attrs(self):
        """---test that Review inherits from BaseModel and has all required base attrs"""
        TestBaseModel.check_base_attributes(self, self.review)


        review_from_storage = storage.get(Review, self.review.id)

    def test_save(self):
        """"---save: persist object to db storage"""
        review = Review(product_id=self.product.id, user_id=self.user.id, comment="Nice", rating=5)
        n_review_inital = len(storage.all(Review))

        # before saving
        self.assertEqual(storage.get(Review, review.id), None)
        self.assertEqual(len(storage.all(Review)), n_review_inital)

        # after saving
        review.save()
        n_review = len(storage.all(Review))
        self.assertNotEqual(None, storage.get(Review, review.id))
        self.assertNotEqual(n_review, n_review_inital)

    def test_delete(self):
        """---delete the current instance from the storage"""

        self.assertNotEqual(None, storage.get(Review, self.review.id))
        self.review.delete()
        self.assertEqual(None, storage.get(Review, self.review.id))

    def test_to_dict(self):
        """---returns a dictionary containing all keys/values of the instance"""
        self.assertIsInstance(self.review.to_dict(), dict)
    
    def test_review_product_relationship(self):
        """---test: review.product should return product for that review"""
        self.assertIsInstance(self.review.product, Product)
        self.assertIsInstance(self.product.reviews, list)
        self.assertEqual(self.product.reviews[0].id, self.review.id)


