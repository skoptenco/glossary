from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Term(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=100, description="ключевое слово (уникальное)")
    description: str = Field(..., min_length=1, description="описание термина")
    created_at: Optional[datetime] = Field(None)
    updated_at: Optional[datetime] = Field(None)

class TermCreate(Term):
    pass

class TermUpdate(BaseModel):
    description: str = Field(..., min_length=1, description="описание термина")

class TermOut(BaseModel):
    keyword: str
    description: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True