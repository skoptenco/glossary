from pydantic import BaseModel, constr, validator
from typing import Optional
from datetime import datetime

KeywordType = constr(strip_whitespace=True, min_length=1, max_length=100)
DescriptionType = constr(strip_whitespace=True, min_length=1, max_length=2000)
RelationType = constr(strip_whitespace=True, min_length=1, max_length=60)

class TermCreate(BaseModel):
    keyword: KeywordType
    description: DescriptionType

    @validator('keyword')
    def lower_keyword(cls, v):
        return v.lower()

class TermUpdate(BaseModel):
    keyword: KeywordType
    description: DescriptionType

    @validator('keyword')
    def lower_keyword(cls, v):
        return v.lower()

class TermDB(BaseModel):
    keyword: KeywordType
    description: DescriptionType
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class Relation(BaseModel):
    id: int
    source_keyword: KeywordType
    target_keyword: KeywordType
    relation_type: RelationType

class RelationCreate (BaseModel):
    source_keyword: KeywordType
    target_keyword: KeywordType
    relation_type: RelationType

    @validator('source_keyword', 'target_keyword')
    def lower_keyword(cls, v):
        return v.lower()

class RelationUpdate(RelationCreate):
    pass