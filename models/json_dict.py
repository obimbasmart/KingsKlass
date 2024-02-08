#!/usr/bin/python

"""
Custom SQLAlchemy type for serializing and deserializing Python dictionaries to and from a database.

This type allows for storing dictionary-like Python objects (in our case a measurement data) in a database column,
converting them to JSON strings for storage and back to dictionaries when retrieved. 

"""

from sqlalchemy.types import TypeDecorator
from sqlalchemy import Text
import json



class JsonEncodedDict(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)
        
measurement_names = [
            "chest/burst", "stomach", "top length", "shoulder",
            "sleeve length", "neck", "muscle", "waist", "laps", "knee"
        ]
default_measurement = {
            name : 0.0 for name in measurement_names
        }