#!/usr/bin/python

"""Measurement Module

This module defines the Measurement class, representing a collection of  Measurement of a user.

Attributes:
    - name (str): Measurement name.
    - value (float): Measurement value.
"""

from models.base_model import BaseModel
from models.measurement import Measurement

class Measurements(BaseModel):
    """Measurement class """

    def __init__(self):
        """get all measurement names from DB and
           create a unique attribute of that measurement
        """

        measurements = Measurement.get_all_measurement_names()

        for measurement in measurements:
            setattr(self, measurement, 0.0)

