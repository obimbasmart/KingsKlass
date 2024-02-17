#!/usr/bin/python3


"""
Unittest  Initialization

initialization code  resets the database before running tests.

The database is reset by dropping it if it exists and creating a new one. 
This ensures a clean and isolated environment for running tests.
"""

from tests.db_access import db_access, storage

db_access.reset_DataBase()
storage.reload()
