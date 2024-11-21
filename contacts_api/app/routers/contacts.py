from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from .. import models, schemas, crud
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.ContactResponse], tags=["Contacts"])
def get_contacts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Contact).filter(models.Contact.owner_id == current_user.id).all()

@router.get("/{contact_id}", response_model=schemas.ContactResponse, tags=["Contacts"])
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    contact = db.query(models.Contact).filter(
        models.Contact.id == contact_id,
        models.Contact.owner_id == current_user.id
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.get("/contacts", response_model=List[schemas.Contact], tags=["Search"])
def read_contacts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    contacts = crud.get_contacts(db, current_user)
    return contacts

@router.get("/contacts/search", response_model=List[schemas.ContactResponse], tags=["Search"])
def search_contacts(
    first_name: Optional[str] = Query(None, max_length=50),
    last_name: Optional[str] = Query(None, max_length=50),
    email: Optional[str] = Query(None, max_length=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Contact).filter(models.Contact.owner_id == current_user.id)
    
    if first_name:
        query = query.filter(models.Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(models.Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(models.Contact.email.ilike(f"%{email}%"))

    results = query.all()
    return results

@router.get("/contacts/birthday-upcoming", response_model=List[schemas.ContactResponse], tags=["Search"])
def get_upcoming_birthdays(
    days: int = Query(7, ge=1, le=365, description="Number of days for upcoming birthdays"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    contacts = crud.get_upcoming_birthdays(db, days, current_user.id)
    if not contacts:
        raise HTTPException(status_code=404, detail="No contacts found with upcoming birthdays")
    return contacts

@router.post("/", response_model=schemas.ContactResponse, status_code=status.HTTP_201_CREATED, tags=["Contacts"])
def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_contact = models.Contact(**contact.dict(), owner_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.put("/{contact_id}", response_model=schemas.ContactResponse, tags=["Contacts"])
def update_contact(
    contact_id: int,
    contact: schemas.ContactUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_contact = db.query(models.Contact).filter(
        models.Contact.id == contact_id,
        models.Contact.owner_id == current_user.id
    ).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/{contact_id}", response_model=schemas.ContactResponse, tags=["Contacts"])
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_contact = db.query(models.Contact).filter(
        models.Contact.id == contact_id,
        models.Contact.owner_id == current_user.id
    ).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return db_contact
