from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float
    stock: int
    rating: float
    brand: str
    description: str
    created_at: datetime

class ProductsResponse(BaseModel):
    total: int
    page: int
    limit: int
    products: list[Product]