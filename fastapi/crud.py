from sqlalchemy.orm import Session
from models import Term
from schemas import TermCreate, TermUpdate
from typing import List, Optional

def get_terms(db: Session, skip: int = 0, limit: int = 100) -> List[Term]:
    return db.query(Term).offset(skip).limit(limit).all()

def get_term_by_keyword(db: Session, keyword: str) -> Optional[Term]:
    return db.query(Term).filter(Term.keyword == keyword).first()

def create_term(db: Session, term_in: TermCreate) -> Term:
    term = Term(
        keyword=term_in.keyword.strip(),
        title=(term_in.title.strip() if term_in.title else None),
        description=term_in.description.strip()
    )
    db.add(term)
    db.commit()
    db.refresh(term)
    return term

def update_term(db: Session, term: Term, updates: TermUpdate) -> Term:
    changed = False
    if updates.title is not None:
        term.title = updates.title.strip() if updates.title else None
        changed = True
    if updates.description is not None:
        term.description = updates.description.strip()
        changed = True
    if changed:
        db.add(term)
        db.commit()
        db.refresh(term)
    return term

def delete_term(db: Session, term: Term) -> None:
    db.delete(term)
    db.commit()