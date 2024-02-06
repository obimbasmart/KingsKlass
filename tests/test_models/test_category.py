#!/usr/bin/python3

"""
    Category Test Module

    This module contains unit tests for the Category-related functionalities.
"""

import unittest
from models import storage
from tests.test_models.test_base_model import TestBaseModel
from models.category import Category
from exceptions.validation_exceptions import NonUniqueValueError

class TestCategory(unittest.TestCase):

    category = None

    def _setup(self, name):
        """---create a new category with name @name"""
        self.category = Category(id=name)
        self.category.save()
        

    def _teardown(self):
        """---delete categorys from storage"""
        self.category.delete()

    def test_base_attrs(self):
        """---test that Category inherits from BaseModel and has all required base attrs"""
        self._setup('Suits')
        TestBaseModel.check_base_attributes(self, self.category)


    def test_no_duplicate(self):
        "---ensure no duplicate category in storage"
        self._setup('Senator')
        n_initial_categorys = len(storage.all(Category))

        with self.assertRaises(NonUniqueValueError) as error:
            self._setup('Senator')

        self.assertEqual(n_initial_categorys, len(storage.all(Category)))

    def test_save(self):
        """"---save: persist object to db storage"""
        category = Category(id="Trouser")
        n_Category_inital = len(storage.all(Category))

        # before saving
        self.assertEqual(storage.get(Category, category.id), None)
        self.assertEqual(len(storage.all(Category)), n_Category_inital)

        # after saving
        category.save()
        n_Category = len(storage.all(Category))
        self.assertNotEqual(None, storage.get(Category, category.id))
        self.assertNotEqual(n_Category, n_Category_inital)

    def test_delete(self):
        """---delete the current instance from the storage"""
        self._setup('Native')
        self.assertNotEqual(None, storage.get(Category, self.category.id))
        self.category.delete()
        self.assertEqual(None, storage.get(Category, self.category.id))

    def test_to_dict(self):
        """---returns a dictionary containing all keys/values of the instance"""
        self._setup('Coperate')
        self.assertIsInstance(self.category.to_dict(), dict)



