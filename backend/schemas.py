from pydantic.v1 import BaseModel

# User schema
class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool

# Product schema
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

# CartItem schema
class CartItem(BaseModel):
    id: int
    product_id: int
    quantity: int
