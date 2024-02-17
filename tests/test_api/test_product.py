#!/usr/bin/python

"""
unit tests for testing the functionality of an product api endpoints.
"""

import requests
import unittest
from os import getenv
from tests.db_access import db_access, storage
from models.user import User


class TestProductAPI(unittest.TestCase):
    """Test product api endpoints"""
    base_url = "http://{}:{}/api/v1".format(getenv("KS_API_HOST"),
                                            getenv("KS_API_PORT"))
    domain_base_url = "http://{}:{}".format(getenv("KS_API_HOST"),
                                            getenv("KS_API_PORT"))

    product_data = {
        "name": "White agbada with kofu cap-test_api",
                "price": 1234,
                "description": "This clothe no be beans, e go well",
                "estimated": 5,
                "categories": ["Senator", "Chinos"],
                "img_url": "api_product_image.png"
    }

    product_id = None
    user = None
    access_token = None
    headers = None

    @classmethod
    def setUpClass(cls):
        cls.admin = User(email=f"admin_test@gmail.com",
                        password="admin_test_pwd", is_admin=True)
        
        # create a normal user
        cls.user = User(email=f"user_test@gmail.com",
                        password="user_test_pwd", is_admin=False)
        
        cls.user.save()
        cls.admin.save()

    def test_get_all_products(self):
        """--- api: get a list of all products"""
        res = requests.get(url=self.base_url + "/products")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

        if res.json():
            self.assertIsInstance(res.json()[0], dict)

    def test_post_product(self):
        """--- api: post a product => only admin should have right to post"""

        #user login
        self.login(data={"email" : self.user.email,
                         "password" : "user_test_pwd"})
        
        res = requests.post(url=self.base_url + "/products",
                            json=self.product_data, headers=self.headers)

        self.assertEqual(res.status_code, 403)
        self.assertIsInstance(res.json(), dict)

        #admin login
        self.login(data={"email" : self.admin.email,
                         "password" : "admin_test_pwd"})
        
        res = requests.post(url=self.base_url + "/products",
                            json=self.product_data, headers=self.headers)

        self.assertEqual(res.status_code, 201)
        self.assertIsInstance(res.json(), dict)
        self.product_id = res.json()["id"]


    def test_missing_data(self):
        """---api: return 400 error if param is missing"""
        attrs = ["name", "price", "description", "estimated", "img_url"]

        self.login(data={"email" : self.admin.email,
                         "password" : "admin_test_pwd"})
   
        for attr in attrs:
            p_data = self.product_data.copy()
            del p_data[attr]
            res = requests.post(url=self.base_url + "/products", json=p_data, headers=self.headers)
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

    def login(self, data):
        """login"""
        res = requests.post(url=self.domain_base_url + "/login", json=data)
        if res.status_code == 200:
            self.access_token = res.json()["access_token"]
            self.headers = {
            "Authorization" : f"Bearer {self.access_token}"
        }
            
        else:
            print("couldn't login")
