from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_contacts(db: Session, current_user: models.User):
    return db.query(models.Contact).filter(models.Contact.owner_id == current_user.id).all()

def get_contact_by_id(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    db_contact = get_contact_by_id(db, contact_id)
    if db_contact:
        for key, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact_by_id(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def get_upcoming_birthdays(db: Session, days: int = 7, owner_id: int = None):
    today = datetime.today().date()
    upcoming_date = today + timedelta(days=days)
    query = db.query(models.Contact).filter(
        models.Contact.birthday >= today,
        models.Contact.birthday <= upcoming_date
    )
    if owner_id:
        query = query.filter(models.Contact.owner_id == owner_id)
    
    return query.all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password,
        first_name=user.first_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
