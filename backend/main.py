from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, auth

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db() -> Session:
    from .database import get_db as db_getter
    db = db_getter()
    try:
        yield db
    finally:
        db.close()

# Seed initial products
products = [
    {"name": "Product 1", "description": "Description 1", "price": 10.0},
    {"name": "Product 2", "description": "Description 2", "price": 20.0},
]

# Create initial products if database is empty
@app.on_event("startup")
def on_startup():
    from .database import SessionLocal
    db = SessionLocal()
    existing_products = db.query(models.Product).count()
    if existing_products == 0:
        for product_data in products:
            new_product = models.Product(**product_data)
            db.add(new_product)
        db.commit()

# Routes for products
@app.get("/products", response_model=List[schemas.Product])
def read_products(db: Session = Depends(get_db)):    return db.query(models.Product).all()

# Add more routes as needed