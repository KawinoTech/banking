from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .config import settings

SECRET_KEY = os.urandom(32)
SECRET_KEY = SECRET_KEY
SQLALCHEMY_DATABASE_URI = f'mysql://{settings.database_username}:{settings.database_password}@{settings.database_host}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

#All models will extend from Base Model
