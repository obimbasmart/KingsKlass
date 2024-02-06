#!/usr/bin/python3

"""
    Order Test Module

    This module contains unit tests for the Order-related functionalities.

    The tests cover various aspects such as Order creation, modification, and validation.
"""

from sqlalchemy import text
from datetime import datetime
import unittest
from models import storage
from tests.test_models.test_base_model import TestBaseModel
from models.measurement import Measurement, NonUniqueValueError

class TestMeasurement(unittest.TestCase):

    measurement = None

    def _setup(self, name):
        """---create a new measurement with name @name"""
        self.measurement = Measurement(name=name)
        self.measurement.save()
        

    def _teardown(self):
        """---delete measurements from storage"""
        self.measurement.delete()

    def test_base_attrs(self):
        """---test that Order inherits from BaseModel and has all required base attrs"""
        self._setup('Waist')
        TestBaseModel.check_base_attributes(self, self.measurement)


    def test_no_duplicate(self):
        "---ensure no duplicate measurement in storage"
        self._setup('Height')
        n_initial_measurements = len(storage.all(Measurement))

        with self.assertRaises(NonUniqueValueError) as error:
            self._setup('Height')

        self.assertEqual(n_initial_measurements, len(storage.all(Measurement)))

    def test_save(self):
        """"---save: persist object to db storage"""
        measurement = Measurement(name="NeckLine")
        n_order_inital = len(storage.all(Measurement))

        # before saving
        self.assertEqual(storage.get(Measurement, measurement.id), None)
        self.assertEqual(len(storage.all(Measurement)), n_order_inital)

        # after saving
        measurement.save()
        n_order = len(storage.all(Measurement))
        self.assertNotEqual(None, storage.get(Measurement, measurement.id))
        self.assertNotEqual(n_order, n_order_inital)

    def test_delete(self):
        """---delete the current instance from the storage"""
        self._setup('Lap')
        self.assertNotEqual(None, storage.get(Measurement, self.measurement.id))
        self.measurement.delete()
        self.assertEqual(None, storage.get(Measurement, self.measurement.id))

    def test_to_dict(self):
        """---returns a dictionary containing all keys/values of the instance"""
        self._setup('Arm')
        self.assertIsInstance(self.measurement.to_dict(), dict)



