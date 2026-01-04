from fastapi import FastAPI, HTTPException, Depends, status
from typing import List
import web.schemas as schemas
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware

from shared.storage import Storage

origins = [
    "http://localhost:5173",
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

@app.get("/terms", response_model=List[schemas.TermOut])
def list_terms(store=Depends(get_storage)):
    return store.list_terms()

@app.get("/terms/{keyword_name}", response_model=schemas.TermOut, status_code=status.HTTP_200_OK)
def read_term(keyword_name: str, store=Depends(get_storage)):
    keyword = store.get_term(keyword_name.strip().lower())
    if not keyword:
        raise HTTPException(status_code=404, detail="Term not found")
    return keyword

@app.post("/terms", response_model=schemas.TermOut, status_code=status.HTTP_201_CREATED)
def create_new_term(term_in: schemas.TermCreate, store=Depends(get_storage)):
    existing = store.get_term(term_in.keyword)
    if existing:
        raise HTTPException(status_code=400, detail="Term with this keyword already exists")
    try:
        term = store.create_term(term_in.keyword, term_in.description)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Integrity error — maybe duplicate keyword")
    return term

@app.put("/terms/{keyword}", response_model=schemas.TermOut)
def update_existing_term(keyword: str, updates: schemas.TermUpdate, store=Depends(get_storage)):
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