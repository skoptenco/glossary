# models.py
from pydantic import BaseModel, constr, validator
from typing import Optional
from datetime import datetime

KeywordType = constr(strip_whitespace=True, min_length=1, max_length=100)

class TermCreate(BaseModel):
    keyword: KeywordType
    description: constr(strip_whitespace=True, min_length=1, max_length=2000)

    @validator('keyword')
    def lower_keyword(cls, v):
        return v.lower()

class TermUpdate(BaseModel):
    keyword: KeywordType
    description: constr(strip_whitespace=True, min_length=1, max_length=2000)

    @validator('keyword')
    def lower_keyword(cls, v):
        return v.lower()

class TermDB(BaseModel):
    keyword: KeywordType
    description: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
