from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TermBase(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=100, description="ключевое слово (уникальное)")
    title: Optional[str] = Field(None, max_length=200)
    description: str = Field(..., min_length=1, description="описание термина")

class TermCreate(TermBase):
    pass

class TermUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None)

class TermOut(BaseModel):
    id: int
    keyword: str
    title: Optional[str]
    description: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True