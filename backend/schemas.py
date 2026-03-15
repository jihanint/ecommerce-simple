from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from .models import User, Product, CartItem

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    image_url: Optional[str] = None
    category: str

class ProductOut(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemOut(CartItemCreate):
    id: int
    product: ProductOut

    class Config:
        from_attributes = True
