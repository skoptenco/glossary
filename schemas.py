from pydantic import BaseModel, constr, validator
from typing import Optional
from datetime import datetime

KeywordType = constr(strip_whitespace=True, min_length=1, max_length=100)
TitleType = constr(strip_whitespace=True, min_length=1, max_length=500)
DescriptionType = constr(strip_whitespace=True, min_length=1, max_length=2000)
MetaDescriptionType = constr(strip_whitespace=True, min_length=1, max_length=2000)
FullDescriptionType = constr(strip_whitespace=True, min_length=1, max_length=5000)
RelationType = constr(strip_whitespace=True, min_length=1, max_length=60)

class TermBase (BaseModel):
    keyword: KeywordType
    title: TitleType
    description: DescriptionType

class TermDetails (BaseModel):
    meta_description: MetaDescriptionType
    full_description: FullDescriptionType

class TermDate (BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class Term (TermBase, TermDate):
    @validator('keyword')
    def lower_keyword(cls, v):
        return v.lower()

class TermDetailed (Term, TermDetails):
    pass

class TermCreate(TermBase, TermDetails):
    pass

class TermUpdate(BaseModel):
    title: Optional[TitleType] = None
    description: Optional[DescriptionType] = None
    meta_description: Optional[MetaDescriptionType] = None
    full_description: Optional[FullDescriptionType] = None

class Relation(BaseModel):
    id: int
    source_keyword: KeywordType
    target_keyword: KeywordType
    relation_type: RelationType

    @validator('source_keyword', 'target_keyword')
    def lower_keyword(cls, v):
        return v.lower()



class RelationCreate (BaseModel):
    source_keyword: KeywordType
    target_keyword: KeywordType
    relation_type: RelationType

    @validator('source_keyword', 'target_keyword')
    def lower_keyword(cls, v):
        return v.lower()

class RelationUpdate(RelationCreate):
    pass