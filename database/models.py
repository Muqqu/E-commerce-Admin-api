from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import date, time, timedelta
from pydantic.fields import Field


class Product(BaseModel):
    __tablename__ = "products"

    name : str
    description : str
    price :float
    category : str
    
    
class Sale(BaseModel):
    __tablename__ = "sales"
 
    product_id : int
    sale_date : date
    quantity : int
    created_at: date

class InventoryUpdate(BaseModel):
    __tablename__ = "inventory"
    product_id: int
    quantity: int
    

