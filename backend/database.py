to_engine = lambda url: create_engine(url, connect_args={"timeout": 30, "keepalive": False})
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./ecommerce.db"

def get_db() -> Session:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()