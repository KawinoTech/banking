from fastapi import FastAPI
from .routes import users, transactions, new_account
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine


#creates all our models/ Though Alembic is an alternative
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(transactions.router)
app.include_router(users.router)
app.include_router(new_account.router)
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_headers = ['*'],
    allow_methods = ['*']
)








