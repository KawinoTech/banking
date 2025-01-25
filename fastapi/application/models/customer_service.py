"""
Customer Service Module.

This module defines models related to customer service interactions, specifically help requests and customer reports. 
The models facilitate tracking and managing customer inquiries and feedback within the system. Each model inherits 
from `BaseModel` for common fields and functionality and integrates with SQLAlchemy ORM for database interactions.

Models:
    - ClientHelpRequest: Represents a help request created by a customer. Tracks the customer's unique identifier, 
      the help message, and its resolution status.
    - ClientReports: Represents a report filed by a customer, such as complaints or feedback. Tracks the customer's 
      unique identifier, report content, and resolution status.

Usage:
    These models can be used to manage customer support tickets and ensure follow-ups on reports or inquiries.
    They provide utility methods to instantiate and represent the objects meaningfully for debugging and logging.

Table Names:
    - client_help: Database table for storing help requests.
    - client_reports: Database table for storing reports filed by customers.

Attributes:
    - owner_customer_no (Foreign Key): Links to the unique identifier of a customer in the customers table.
    - text (Text): Stores the description or message related to the help request or report.
    - status_resolved (Boolean): Tracks if the item has been addressed; defaults to unresolved (False).
"""

from .base_model import BaseModel
from . import Base
from sqlalchemy import Column, Text, Integer, ForeignKey, Boolean

class ClientHelpRequest(BaseModel, Base):
    """
    Represents a help request created by a customer.

    Inherits from:
        - BaseModel: Common functionality for models.
        - Base: SQLAlchemy base class for ORM mapping.

    Attributes:
        __tablename__ (str): The name of the table in the database ("client_help").
        owner_customer_no (Column): The customer's unique identifier, foreign key linked to the customers table.
        text (Column): The message or description of the help request.
        status_resolved (Column): Indicates whether the help request has been resolved. Defaults to False.
    """
    __tablename__ = "client_help"
    
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'), index=True)
    text = Column(Text, nullable=False)
    status_resolved = Column(Boolean, nullable=False, default=False)

    def __init__(self, *args, **kwargs):
        """
        Initializes the ClientHelpRequest object with provided arguments.

        Args:
            *args: Variable positional arguments for the superclass.
            **kwargs: Variable keyword arguments for the superclass.
        """
        super().__init__(*args, **kwargs)

    def __repr__(self):
        """
        Returns a string representation of the help request.

        Returns:
            str: The `text` field of the help request.
        """
        return f"{self.text}"


class ClientReports(BaseModel, Base):
    """
    Represents a report created by a customer.

    Inherits from:
        - BaseModel: Common functionality for models.
        - Base: SQLAlchemy base class for ORM mapping.

    Attributes:
        __tablename__ (str): The name of the table in the database ("client_reports").
        owner_customer_no (Column): The customer's unique identifier, foreign key linked to the customers table.
        text (Column): The message or description of the report.
        status_resolved (Column): Indicates whether the report has been resolved. Defaults to False.
    """
    __tablename__ = "client_reports"
    
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'), index=True)
    text = Column(Text, nullable=False)
    status_resolved = Column(Boolean, nullable=False, default=False)

    def __init__(self, *args, **kwargs):
        """
        Initializes the ClientReports object with provided arguments.

        Args:
            *args: Variable positional arguments for the superclass.
            **kwargs: Variable keyword arguments for the superclass.
        """
        super().__init__(*args, **kwargs)

    def __repr__(self):
        """
        Returns a string representation of the report.

        Returns:
            str: The `text` field of the report.
        """
        return f"{self.text}"
