from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from .. import models, schemas
from ..database import get_db
from ..crud import get_upcoming_birthdays

router = APIRouter()

# Создание нового контакта
@router.post("/", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Получение списка всех контактов
@router.get("/", response_model=List[schemas.ContactResponse])
def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return contacts

# Получение одного контакта по ID
@router.get("/{contact_id}", response_model=schemas.ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

# Обновление контакта по ID
@router.put("/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Удаление контакта по ID
@router.delete("/{contact_id}", response_model=schemas.ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(db_contact)
    db.commit()
    return db_contact

# Поиск контактов по имени, фамилии или email
@router.get("/search", response_model=List[schemas.ContactResponse])
def search_contacts(
    first_name: Optional[str] = Query(None, max_length=50),
    last_name: Optional[str] = Query(None, max_length=50),
    email: Optional[str] = Query(None, max_length=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.Contact)
    
    if first_name:
        query = query.filter(models.Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(models.Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(models.Contact.email.ilike(f"%{email}%"))
    
    contacts = query.all()
    return contacts

# Получение ближайших дней рождения
@router.get("/contacts/birthday-upcoming", response_model=List[schemas.ContactResponse])
def get_upcoming_birthdays_endpoint(
    db: Session = Depends(get_db),
    days: int = Query(7, ge=1, le=365, description="Number of days for upcoming birthdays")
):
    contacts = get_upcoming_birthdays(db, days)
    
    if not contacts:
        raise HTTPException(status_code=404, detail="No contacts found with upcoming birthdays")
    
    return contacts


