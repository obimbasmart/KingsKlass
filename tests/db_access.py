#!/user/bin/python3

"""Setup connection to DB_storage for testing"""

import os
from models import storage
from models.base_model import Base
from sqlalchemy import text

class DBAccessLayer:
    
    def __init__(self):
        self.connection = storage.engine.connect()
        self.session = storage.session

    def reset_DataBase(self):
        """Drop the database and recreate it"""
        self.connection.execute(text('DROP DATABASE IF EXISTS kingsklass_test_db;'))
        self.connection.execute(text('CREATE DATABASE IF NOT EXISTS kingsklass_test_db;'))

db_access = DBAccessLayer()