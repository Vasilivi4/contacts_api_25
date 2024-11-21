from fastapi import FastAPI
from .routers import contacts, auth
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(contacts.router)
app.include_router(auth.router)