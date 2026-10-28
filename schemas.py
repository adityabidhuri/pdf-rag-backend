from pydantic import BaseModel ,EmailStr,Field,ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    email:EmailStr
    password:str=Field(min_length=8,max_length=128)

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class DocumentResponse(BaseModel):
    id: int
    filename: str
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)