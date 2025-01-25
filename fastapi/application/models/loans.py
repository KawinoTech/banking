"""
Loan Models Documentation

This module defines the SQLAlchemy ORM models for managing loans within the application. It includes models for 
personal loans, business loans, and mortgages, inheriting common attributes from a base Loan model.

Modules and Dependencies:
- SQLAlchemy ORM for database model definition.
- Models for document relationships: `LoanDocs`, `MortgageDocs`.
- Base models and database session management.

Classes:
    - `Loan`: Abstract base class for loan-related models.
    - `PersonalLoans`: Represents personal loans, extending `Loan`.
    - `BusinessLoans`: Represents business loans, extending `Loan`.
    - `Mortgages`: Represents mortgages, extending `Loan`.

Attributes and Relationships:
    Each subclass of `Loan` has unique attributes and relationships tailored to its specific use case.
"""

from . import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Text, DateTime
from .base_model import BaseModel
from sqlalchemy.orm import relationship
from babel.numbers import format_currency
from .files import LoanDocs, MortgageDocs


class Loan(BaseModel):
    """
    Abstract base class representing common attributes for all loan types.

    Attributes:
        account_no (str): Unique identifier for the loan account.
        owner_customer_no (int): Foreign key linking to the associated customer.
        payback_period (int): Loan payback duration in months.
        rate (float): Interest rate for the loan.
        amount (float): Total loan amount.
        currency (str): Currency code, default is "KES".
        account_status (str): Current loan status, e.g., "in-review".
        maturity_date (datetime): Date when the loan matures.
        compounding_frequency (str): Frequency of interest compounding, default is "daily".
        last_calculation_date (datetime): Date of the last interest calculation.
        next_calculation_date (datetime): Date for the next interest calculation.
        outstanding_amount (float): Remaining amount to be paid.
        purpose (str): Purpose for which the loan was taken.
        accrued_interest (float): Total interest accrued.
        principal_paid (float): Amount of the principal paid.

    Methods:
        truncate_uuid(): Truncates the UUID format of the `account_no` for display purposes.
    """
    account_no = Column(String(100), nullable=False, primary_key=True)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    payback_period = Column(Integer, nullable=False)
    rate = Column(Float, nullable=False, default=7.45)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False, default="KES")
    account_status = Column(String(15), nullable=False, default="in-review")
    maturity_date = Column(DateTime, nullable=False)
    compounding_frequency = Column(String(20), nullable=False, default="daily")
    last_calculation_date = Column(DateTime, nullable=False)
    next_calculation_date = Column(DateTime, nullable=False)
    outstanding_amount = Column(Float, nullable=False)
    purpose = Column(Text, nullable=False)
    accrued_interest = Column(Float, nullable=False, default=0.00)
    principal_paid = Column(Float, nullable=False, default=0.00)

    def truncate_uuid(self):
        """
        Truncates the UUID format of the `account_no` for display purposes.
        """
        uuid = self.account_no
        parts = uuid.split('-')
        self.account_no = f"{parts[0]}-***-{parts[-1][-2:]}"

    def format_cash(self):
        """
        Formats the account balance into a readable currency string (USD).
        """
        self.disposable_amount = format_currency(self.disposable_amount, 'USD', locale='en_US')
        self.outstanding_amount = format_currency(self.outstanding_amount, 'USD', locale='en_US')
        self.amount = format_currency(self.amount, 'USD', locale='en_US')
class PersonalLoans(Loan, Base):
    """
    Represents a personal loan.

    Attributes:
        employment_status (str): Employment status of the borrower.
        disposable_amount (float): Disposable income of the borrower.
        monthly_income (int): Borrower's monthly income.
        account_type (str): Account type, default is "Personal Loan".
    """
    __tablename__ = "personal_loans"
    employment_status = Column(String(20), nullable=False)
    disposable_amount = Column(Float, nullable=False)
    monthly_income = Column(Integer, nullable=False)
    account_type = Column(String(100), nullable=False, default="Personal Loan")


class BusinessLoans(Loan, Base):
    """
    Represents a business loan.

    Attributes:
        id_no (str): Identification number of the business owner.
        address (str): Business address.
        pmargin (float): Profit margin for the business.
        dob (datetime): Date of birth of the owner.
        disposable_amount (float): Disposable income of the business.
        account_type (str): Account type, default is "Business Loan".
        loan_documents (relationship): Relationship to associated `LoanDocs` for business loan documents.
    """
    __tablename__ = "business_loans"
    id_no = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)
    pmargin = Column(Float, nullable=False)
    dob = Column(DateTime, nullable=False)
    disposable_amount = Column(Float, nullable=False)
    account_type = Column(String(100), nullable=False, default="Business Loan")
    loan_documents = relationship("LoanDocs", backref="business_loan_document")


class Mortgages(Loan, Base):
    """
    Represents a mortgage loan.

    Attributes:
        employment_status (str): Employment status of the borrower.
        annual_income (float): Annual income of the borrower.
        payback_period (int): Payback period in years.
        property_address (str): Address of the mortgaged property.
        property_value (float): Value of the property.
        down_payment (float): Initial down payment for the property.
        account_type (str): Account type, default is "Mortgage".
        property_type (str): Type of the property being mortgaged.
        loan_documents (relationship): Relationship to associated `MortgageDocs` for mortgage-related documents.
    """
    __tablename__ = "mortgages"
    employment_status = Column(String(20), nullable=False)
    annual_income = Column(Float, nullable=False)
    payback_period = Column(Integer, nullable=False)
    property_address = Column(String(20), nullable=False)
    property_value = Column(Float, nullable=False)
    down_payment = Column(Float, nullable=False)
    account_type = Column(String(100), nullable=False, default="Mortgage")
    property_type = Column(String(20), nullable=False)
    loan_documents = relationship("MortgageDocs", backref="mortgage_document")
