from fastapi import FastAPI
from .routers import contacts
from .database import engine
from . import models

# Створення всіх таблиць
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Підключення роутера для контактів
app.include_router(contacts.router)
