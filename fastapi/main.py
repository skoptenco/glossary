from fastapi import FastAPI, HTTPException, Depends, status
from typing import List
import models, crud, schemas
from database import SessionLocal, engine, Base
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Glossary API", version="1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/terms", response_model=List[schemas.TermOut])
def list_terms(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    terms = crud.get_terms(db, skip=skip, limit=limit)
    return terms

@app.get("/terms/{keyword}", response_model=schemas.TermOut)
def read_term(keyword: str, db=Depends(get_db)):
    term = crud.get_term_by_keyword(db, keyword)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term

@app.post("/terms", response_model=schemas.TermOut, status_code=status.HTTP_201_CREATED)
def create_new_term(term_in: schemas.TermCreate, db=Depends(get_db)):
    # проверка существования:
    existing = crud.get_term_by_keyword(db, term_in.keyword)
    if existing:
        raise HTTPException(status_code=400, detail="Term with this keyword already exists")
    try:
        term = crud.create_term(db, term_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error — maybe duplicate keyword")
    return term

@app.put("/terms/{keyword}", response_model=schemas.TermOut)
def update_existing_term(keyword: str, updates: schemas.TermUpdate, db=Depends(get_db)):
    term = crud.get_term_by_keyword(db, keyword)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    term = crud.update_term(db, term, updates)
    return term

@app.delete("/terms/{keyword}", status_code=status.HTTP_204_NO_CONTENT)
def delete_term(keyword: str, db=Depends(get_db)):
    term = crud.get_term_by_keyword(db, keyword)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    crud.delete_term(db, term)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)