from fastapi import FastAPI,Depends
from database import get_db,Base,engine,db_dependency,Base
from sqlalchemy.orm import Session
from sqlalchemy import text
import models
from auth import router as auth_router
from documents import router as documents_router


app = FastAPI(
    title="PDF RAG Backend",
    description="An API for uploading PDFs and asking questions about them.",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(documents_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def home():
    return {"message": "PDF RAG Backend is running!"}


@app.get("/health/database")
def check_database(db: db_dependency):
    db.execute(text("SELECT 1"))

    return {"message": "Database connection successful!"}
