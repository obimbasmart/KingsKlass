#!/usr/bin/python

"""
unit tests for testing the functionality of an product api endpoints.
"""

import requests
import unittest
from os import getenv
from tests.db_access import db_access, storage


class TestProductAPI(unittest.TestCase):
    """Test product api endpoints"""
    base_url = "http://{}:{}/api/v1".format(getenv("KS_API_HOST"),
                                     getenv("KS_API_PORT"))
    
    product_data = {
                "name": "White agbada with kofu cap-test_api",
                "price": 1234,
                "description": "This clothe no be beans, e go well",
                "estimated" : 5,
                "categories" : ["Senator", "Chinos"],
                "img_url" : "api_product_image.png"
    }

    product_id = None

    @classmethod
    def setUpClass(cls):
        db_access.reset_DataBase()
        storage.reload()

    def test_get_all_products(self):
        """--- api: get a list of all products"""
        res = requests.get(url=self.base_url + "/products")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

        if res.json():
            self.assertIsInstance(res.json()[0], dict)

    def test_post_product(self):
        """--- api: post a product"""
        res = requests.post(url=self.base_url + "/products",
                            json = self.product_data)
        
        self.assertEqual(res.status_code, 201)
        self.assertIsInstance(res.json(), dict)
        self.product_id = res.json()["id"]

    def test_missing_data(self):
        """---api: return 400 error if param is missing"""
        attrs = ["name", "price", "description", "estimated", "img_url"]
    
        for attr in attrs:
            p_data = self.product_data.copy()
            del p_data[attr]
            res = requests.post(url=self.base_url + "/products", json = p_data)
            self.assertEqual(res.status_code, 400)
            self.assertIn(f"Missing {attr}", res.text)
        
    def test_get_product_by_id(self):
        """--- api: get a specific product by id"""
        if self.product_id is None:
            self.test_post_product()

        res = requests.get(url=self.base_url + f"/products/{self.product_id}")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), dict)
        self.assertEqual(self.product_id, res.json()["id"])
