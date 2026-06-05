from pydantic import BaseModel ,Field 
from datetime import datetime
from enum import Enum
class CategoryEnum(str, Enum):
    electronics = "electronics"
    books = "books"
    clothing = "clothing"

category_map={ "electronics":1,
    "books":2,
    "clothing":3}

class Catagories(BaseModel):
    name:str
    description:str
    model_config = {
        "from_attributes": True
    }

class Product(BaseModel):    
    name:str
    description:str
    price:float
    quantity:int
    model_config = {
        "from_attributes": True
    }

class ProductCreate(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "iPhone"})
    description: str = Field(None, json_schema_extra={"example": "Apple phone"})
    price: float = Field(..., json_schema_extra={"example": 1200})
    quantity: int = Field(..., json_schema_extra={"example": 5})