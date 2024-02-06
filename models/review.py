#!/usr/bin/python3

"""
Review Module

This module defines the `Review` class, representing user reviews for products.

Attributes:
    - product_id (int): The unique identifier of the reviewed product.
    - user_id (str): The unique identifier of the user who submitted the review.
    - comment (str): The textual comment provided by the user.
    - rating (int): The numerical rating given by the user (1 to 5).
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """Review class """
    
    __tablename__ = 'reviews'
    product_id = Column(String(60), ForeignKey('products.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    comment = Column(String(1024),  nullable=False)
    rating = Column(Integer, nullable=False)

    # relationships
    product = relationship('Product', back_populates='reviews')