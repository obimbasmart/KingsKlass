#!/usr/bin/python

"""
unit tests for testing the functionality of an product api endpoints.
"""

import requests
import unittest
from os import getenv
from tests.db_access import storage
from models.user import User
from models.json_dict import default_measurement


class TestUserAPI(unittest.TestCase):
    """Test product api endpoints"""
    base_url = "http://{}:{}/api/v1".format(getenv("KS_API_HOST"),
                                            getenv("KS_API_PORT"))
    domain_base_url = "http://{}:{}".format(getenv("KS_API_HOST"),
                                            getenv("KS_API_PORT"))

    user_data = {
        "email": "new_user@gmail.com", "password": "new_user_pwd", "username": "Breadwinner"
    }

    user_id = None
    user = None
    access_token = None
    headers = None

    @classmethod
    def setUpClass(cls):
        # create a new admin user
        cls.admin = User(email=f"admin_test@gmail.com",
                         password="admin_test_pwd",
                         is_admin=True, username="KingsKlass")

        # create a normal user
        cls.user = User(email=f"user_test@gmail.com",
                        password="user_test_pwd", is_admin=False, username="Breadwinner02")

        cls.user.save()
        cls.admin.save()

    def test_get_all_users(self):
        """--- api: get a list of all users"""

        # normal user login
        self.login(data={"email": self.user.email,
                         "password": "user_test_pwd"})

        # shouldn't work, admin required
        res = requests.get(url=self.base_url + "/users", headers=self.headers)
        self.assertEqual(res.status_code, 403)

        # admin login
        self.login(data={"email": self.admin.email,
                         "password": "admin_test_pwd"})
        # should work
        res = requests.get(url=self.base_url + "/users", headers=self.headers)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_get_user_by_id(self):
        """--- api: get a user by ID"""
        # admin login
        # admin login
        self.login(data={"email": self.admin.email,
                         "password": "admin_test_pwd"})

        res = requests.get(url=self.base_url +
                           f"/users/{self.user.id}", headers=self.headers)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), dict)

    def test_create_user(self):
        """--- api: create a new user"""

        res = requests.post(url=self.domain_base_url + "/register",
                            json=self.user_data)

        self.assertEqual(res.status_code, 201)
        self.assertIsInstance(res.json(), dict)
        user = storage.get_user(self.user.email)

    def test_get_user_measurements(self):
        """--- api: get a specific user measurements"""
        # normal user login
        self.login(data={"email": self.user.email,
                         "password": "user_test_pwd"})

        res = requests.get(url=self.base_url + f"/users/{self.user.id}/measurements",
                           headers=self.headers)

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), dict)
        self.assertDictEqual(res.json(), default_measurement)

    def login(self, data):
        """login"""
        res = requests.post(url=self.domain_base_url + "/login", json=data)
        if res.status_code == 200:
            self.access_token = res.json()["access_token"]
            self.headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

        else:
            print("couldn't login")
