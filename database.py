from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase,Session
from typing import Annotated

# Database file location
DATABASE_URL = "sqlite:///./pdf_rag.db"

# Create the database engine
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False},)

# Create a factory for database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Base class for our database models
class Base(DeclarativeBase):
    pass


# Provide a database session to API endpoints
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
