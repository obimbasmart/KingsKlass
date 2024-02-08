#!/usr/bin/python

"""Order Module

This module defines the Order class, an actual order placed by a user

Attributes:
    - product_id (int): The unique identifier of the ordered product.
    - user_id (string) : Unique identifier of the user who ordered the product
    - price (float): The price of the product.
    - description (str): A brief description of the product.
    - estimated (int): number of days required to get the product ready
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Enum, ForeignKey, Table, JSON
from models.json_dict import JsonEncodedDict, default_measurement

class Order(BaseModel, Base):
    """Order class """

    __tablename__ = 'orders'
    product_id = Column(String(60), ForeignKey('products.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    
    order_status = Column(Enum('PENDING', 'COMFIRMED', 'COMPLETED', 'IN_PRGRESS', 'DELIVERED', name='OrderStatus'),
                          default='PENDING')
    
    order_progress = Column(Enum('AWAITING_COMFIRMATION', 'MATERIAL_SOURCING', 'CUTTING', 'SEWING', 'IRONING', 'PACKAGING', name='OrderStatus'),
                          default='AWAITING_COMFIRMATION')
    
    additional_info = Column(String(1024), nullable=True)

    # relationships
    measurements = Column(JsonEncodedDict, default=default_measurement)

    # def to_dict(self):
    #     order_dict = super().to_dict()

    #     measurements = order_dict.get("measurements")

    #     if measurements:
    #         order_dict["measurements"] = measurements.to_dict()

    #     return order_dict