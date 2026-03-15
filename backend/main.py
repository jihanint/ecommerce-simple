from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from backend.database import engine, get_db, Base
from backend.models import User, Product, CartItem
from backend.schemas import UserCreate, UserOut, Token, ProductOut, CartItemCreate, CartItemOut
from backend.auth import (
    create_access_token,
    verify_password,
    get_password_hash,
    get_current_user
)

app = FastAPI(title="E-Commerce API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed products on startup
@app.on_event("startup")
def seed_products():
    with Session(engine) as session:
        if not session.query(Product).first():
            products = [
                Product(
                    name="Wireless Headphones",
                    description="High-quality wireless headphones with noise cancellation",
                    price=79.99,
                    image_url="https://example.com/headphones.jpg",
                    category="Electronics"
                ),
                Product(
                    name="Smart Watch",
                    description="Fitness tracking smartwatch with heart rate monitor",
                    price=199.99,
                    image_url="https://example.com/smartwatch.jpg",
                    category="Electronics"
                ),
                Product(
                    name="Running Shoes",
                    description="Lightweight running shoes for all terrains",
                    price=129.99,
                    image_url="https://example.com/shoes.jpg",
                    category="Sports"
                ),
                Product(
                    name="Backpack",
                    description="Durable backpack with laptop compartment",
                    price=59.99,
                    image_url="https://example.com/backpack.jpg",
                    category="Accessories"
                ),
                Product(
                    name="Sunglasses",
                    description="UV protection sunglasses with polarized lenses",
                    price=89.99,
                    image_url="https://example.com/sunglasses.jpg",
                    category="Accessories"
                ),
                Product(
                    name="Yoga Mat",
                    description="Non-slip yoga mat for home workouts",
                    price=34.99,
                    image_url="https://example.com/yogamat.jpg",
                    category="Sports"
                ),
            ]
            session.add_all(products)
            session.commit()

# Health check
@app.get("/")
def read_root():
    return {"message": "E-Commerce API is running", "status": "ok"}

# User registration
@app.post("/users", response_model=UserOut)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user_data.email)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get all products
@app.get("/products", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

# Get product by ID
@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

# Add item to cart
@app.post("/cart", response_model=CartItemOut)
def add_to_cart(
    cart_item_data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == cart_item_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == cart_item_data.product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = CartItem(
            product_id=cart_item_data.product_id,
            user_id=current_user.id,
            quantity=cart_item_data.quantity
        )
        db.add(new_item)
    
    db.commit()
    db.refresh(existing_item or new_item)
    return existing_item or new_item

# Get user cart
@app.get("/cart", response_model=List[CartItemOut])
def get_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == current_user.id
    ).all()
    return cart_items

# Remove item from cart
@app.delete("/cart/{item_id}", response_model=CartItemOut)
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    db.delete(item)
    db.commit()
    return item

# Get cart total
@app.get("/cart/total", response_model=dict)
def get_cart_total(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == current_user.id
    ).all()
    
    total = sum(item.quantity * db.query(Product).get(item.product_id).price for item in cart_items)
    return {"total": round(total, 2)}
