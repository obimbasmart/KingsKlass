#!/usr/bin/python3
"""This module defines a class to manage database storage for KingsKlass"""

from models.base_model import Base

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from models.category import Category
from models.order import Order
from models.product import Product
from models.review import Review
from models.user import User


class DBStorage:
    """This class manages storage of hbnb models in JSON format"""
    __engine = None
    __session = None
    __Session = None

    if os.environ.get('KS_ENV') == 'test':
        os.environ['KS_MYSQL_USER'] = os.environ.get('KS_MYSQL_TEST_USER')
        os.environ['KS_MYSQL_PWD'] = os.environ.get('KS_MYSQL_TEST_PWD')
        os.environ['KS_MYSQL_DB'] = os.environ.get('KS_MYSQL_TEST_DB')

    def __init__(self):
        """create engine and session for db storage"""
        self.__engine = \
            create_engine('mysql+mysqldb://{}:{}@{}/{}'
                          .format(os.environ.get("KS_MYSQL_USER"),
                                  os.environ.get("KS_MYSQL_PWD"),
                                  os.environ.get("KS_MYSQL_HOST"),
                                  os.environ.get("KS_MYSQL_DB")),
                          pool_pre_ping=True)

    @property
    def engine(self):
        return self.__engine
    
    @property
    def session(self):
        return self.__session

    def all(self, cls=None):
        """Returns a dictionary of objects currently in database"""
        all_models = [Category, Product, Review, User, Order]
        if cls is None:
            all_objects = {}
            for klass in all_models:
                klass_objects = self.__session.query(klass).all()
                all_objects.update({obj.__class__.__name__ + '.' +
                                    obj.id: obj for obj in klass_objects})
            return all_objects

        return {obj.__class__.__name__ + '.' + obj.id:
                obj for obj in self.__session.query(cls).all()}

    def new(self, obj):
        """Adds new object to the current database session"""
        self.__session.add(obj)

    def delete(self, obj=None):
        """delete @obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__Session = scoped_session(session_factory)
        self.__session = self.__Session()


    def close(self):
        """close session"""
        self.__Session.remove()


    def get(self, cls, id):
        """
        Retrieve one object from a class
        attr:
            cls: The class to get
            id: object's unique id
        """
        if type(cls) == str:
            key = cls + "." + id
        else:
            key = cls.__name__ + "." + id

        instances_dict = self.all(cls)
        clsInstance = instances_dict.get(key)
        return clsInstance
    
    def get_user(self, email):
        """get user by email"""
        user = self.__session.query(User).filter(User.email == email).first()
        return user
