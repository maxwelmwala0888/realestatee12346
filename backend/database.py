print(">>> database.py STARTED")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

print(">>> imports OK")

DATABASE_URL = "sqlite:///./realty.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

print(">>> engine created")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

print(">>> SessionLocal created")

Base = declarative_base()

print(">>> Base created")
