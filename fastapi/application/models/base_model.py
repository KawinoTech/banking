from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, DateTime,String
class BaseModel():
    def __init__(self, *args, **kwargs):
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    id = Column(String(36), nullable=False, primary_key=True, unique=True, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False, onupdate=datetime.now())