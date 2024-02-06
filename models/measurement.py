#!/usr/bin/python

"""Measurement Module

This module defines the Measurement class, representing a unique Measurement of a user.

Attributes:
    - name (str): Measurement name.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import validates
from exceptions.validation_exceptions import NonUniqueValueError

class Measurement(BaseModel, Base):
    """Measurement class """
    __tablename__ = 'measurements'
    name = Column(String(60), nullable=False, unique=True)

    @validates("name")
    def validate_name(self, key, value):    
        all_names = Measurement.get_all_measurement_names()
        if value  not in all_names:
            return value
        raise NonUniqueValueError(f"measurement: {value} must be unique")
    

    @classmethod
    def get_all_measurement_names(cls):
        """get a list of all measurement names in storage"""
        from models import storage
        return [m.name for m in storage.all(Measurement).values()]
