from uuid import UUID

from fastapi import FastAPI, HTTPException, Depends, status
from typing import List
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware

from shared.storage import Storage
from shared.models import TermDB, TermCreate, TermUpdate, RelationCreate, RelationUpdate, Relation

origins = [
    "http://localhost:5173",
    "http://localhost:80",
]

app = FastAPI(title="Glossary API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)

storage = Storage("web/glossary.db")

def get_storage() -> Storage:
    return storage

@app.get("/terms", response_model=List[TermDB], status_code=status.HTTP_200_OK)
def list_terms(store=Depends(get_storage)):
    return store.list_terms()

@app.get("/terms/{keyword_name}", response_model=TermDB, status_code=status.HTTP_200_OK)
def read_term(keyword_name: str, store=Depends(get_storage)):
    keyword = store.get_term(keyword_name.strip().lower())
    if not keyword:
        raise HTTPException(status_code=404, detail="Term not found")
    return keyword

@app.post("/terms", response_model=TermDB, status_code=status.HTTP_201_CREATED)
def create_new_term(term_in: TermCreate, store=Depends(get_storage)):
    existing = store.get_term(term_in.keyword)
    if existing:
        raise HTTPException(status_code=400, detail="Term with this keyword already exists")
    try:
        term = store.create_term(term_in.keyword, term_in.description)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Integrity error — maybe duplicate keyword")
    return term

@app.put("/terms/{keyword}", response_model=TermDB, status_code=status.HTTP_202_ACCEPTED)
def update_existing_term(keyword: str, updates: TermUpdate, store=Depends(get_storage)):
    term = store.get_term(keyword)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    term = store.update_term(keyword, updates.description)
    return term

@app.delete("/terms/{keyword}", status_code=status.HTTP_204_NO_CONTENT)
def delete_term(keyword: str, store=Depends(get_storage)):
    term = store.get_term(keyword)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    store.delete_term(keyword)
    return 204

@app.get("/relations", response_model=List[Relation], status_code=status.HTTP_200_OK)
def list_relations(store =Depends(get_storage)):
    return store.list_relations()

@app.get("/relations/{relation_id}", response_model=Relation, status_code=status.HTTP_200_OK)
def get_relation(relation_id: UUID, store=Depends(get_storage)):
    relation = store.get_relation(relation_id)
    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")
    return relation

@app.post("/relations", response_model=Relation, status_code=status.HTTP_201_CREATED)
def create_new_relation(relation_in: RelationCreate, store=Depends(get_storage)):
    try:
        relation = store.create_relation(relation_in.source_keyword, relation_in.target_keyword, relation_in.relation_type)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Integrity error")
    return relation

@app.put("/relations/{relation_id}", response_model=Relation, status_code=status.HTTP_202_ACCEPTED)
def update_existing_relation(relation_id: int, updates: RelationUpdate, store=Depends(get_storage)):
    term = store.get_relation(relation_id)
    if not term:
        raise HTTPException(status_code=404, detail="Relation not found")
    term = store.update_relation(relation_id, updates.source_keyword, updates.target_keyword, updates.relation_type)
    return term

@app.delete("/relations/{relation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relation(relation_id: int, store=Depends(get_storage)):
    term = store.get_relation(relation_id)
    if not term:
        raise HTTPException(status_code=404, detail="Relation not found")
    store.delete_relation(relation_id)
    return 204