#!/usr/bin/python

"""Product Module

This module defines the Product class, representing items available for sale.

Attributes:
    - name (str): The name of the product.
    - price (float): The price of the product.
    - description (str): A brief description of the product.
    - estimated (int): number of days required to get the product ready
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, Integer, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship


# Define the association table for the many-to-many relationship
product_category = Table(
    'product_category',
    Base.metadata,
    Column('product_id', String(60), ForeignKey('products.id')),
    Column('category_id', String(60), ForeignKey('categories.id'))
)

class Product(BaseModel, Base):
    """Product class """
    
    __tablename__ = 'products'
    name = Column(String(128), nullable=False)
    price = Column(Float,  nullable=False)
    description = Column(String(1024), nullable=False)
    img_url = Column(String(1024), nullable=False)
    estimated = Column(Integer, nullable=True)
    on_draft = Column(Boolean, default=False, nullable=False)
    # relationships
    reviews = relationship('Review', back_populates='product')
    categories = relationship('Category', secondary=product_category, back_populates="products")


    def to_dict(self):
        p_dict =  super().to_dict()
        if p_dict.get("categories"):
            p_dict['categories'] = [c.to_dict() for c in p_dict['categories']]
        return p_dict