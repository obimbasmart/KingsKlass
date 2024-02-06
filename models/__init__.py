#!/usr/bin/python3

"""
reload/init objects from DB
"""

from dotenv import load_dotenv
from os import getenv

load_dotenv()
if getenv("KS_TYPE_STORAGE", None) == 'db':
    from models.storage_engine.db_storage import DBStorage
    storage = DBStorage()

storage.reload()