"""
Base Model Module.

This module defines the `BaseModel` class, a foundational ORM model for SQLAlchemy-based applications.
It provides common fields and functionality such as ID, creation timestamp, and updated timestamp for derived models.
"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, DateTime, String

class BaseModel:
    """
    BaseModel Class.

    This class serves as a base for ORM models, providing shared fields such as `id`, `created_at`, 
    and `updated_at`. It also includes functionality to initialize an object with keyword arguments.

    Attributes:
        id (str): A universally unique identifier for the object. Automatically generated.
        created_at (datetime): Timestamp of when the object was created. Defaults to the current time.
        updated_at (datetime): Timestamp of the last update to the object. Automatically updated when the object changes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes an instance of BaseModel.

        Args:
            *args: Positional arguments (not used, for flexibility).
            **kwargs: Keyword arguments to initialize attributes dynamically.

        Examples:
            obj = BaseModel(name="Test Object", status="active")
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    # Common database columns for all derived models
    id = Column(String(36), nullable=False, primary_key=True, unique=True, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False, onupdate=datetime.now())
