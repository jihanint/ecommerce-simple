from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from .database import engine, Base, get_db
from .models import User, Product, CartItem
from .schemas import UserCreate, UserOut, Token, ProductOut, CartItemCreate, CartItemOut
from .auth import create_access_token, get_current_user, verify_password, get_password_hash
import httpx

app = FastAPI(title=\
