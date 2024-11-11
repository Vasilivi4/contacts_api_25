from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta

# Получение списка контактов с пагинацией
def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Contact).offset(skip).limit(limit).all()

# Получение контакта по ID
def get_contact_by_id(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

# Создание нового контакта
def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Обновление контакта по ID
def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    db_contact = get_contact_by_id(db, contact_id)
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
    return db_contact

# Удаление контакта по ID
def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact_by_id(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

# Получение ближайших дней рождения в интервале от 1 до 365 дней
def get_upcoming_birthdays(db: Session, days: int = 7):
    today = datetime.today().date()  # Текущая дата без времени
    upcoming_date = today + timedelta(days=days)
    
    # Запрос контактов с днями рождения в указанном интервале
    return db.query(models.Contact).filter(
        models.Contact.birthday >= today,
        models.Contact.birthday <= upcoming_date
    ).all()
