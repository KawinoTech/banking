from ..database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Text, DateTime
from .base_model import BaseModel
from sqlalchemy.orm import relationship
from .files import LoanDocs, MortgageDocs


class Loan(BaseModel):

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
        uuid = self.account_no
        parts = uuid.split('-')
        truncated = f"{parts[0]}-***-{parts[-1][-2:]}"
        self.account_no = truncated
class PersonalLoans(Loan, Base):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    __tablename__ = "personal_loans"
    employment_status = Column(String(20), nullable=False)
    disposable_amount = Column(Float, nullable=False)
    monthly_income = Column(Integer, nullable=False)
    loan_type = Column(String(100), nullable=False, default="Personal Loan")

class BusinessLoans(Loan, Base):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    __tablename__ = "business_loans"
    id_no = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)
    pmargin = Column(Float, nullable=False)
    dob = Column(DateTime, nullable=False)
    disposable_amount = Column(Float, nullable=False)
    loan_type = Column(String(100), nullable=False, default="Business Loan")
    loan_documents = relationship("LoanDocs", backref="business_loan_document")

class Mortgages(Loan, Base):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    __tablename__ = "mortgages"
    loan_documents = relationship("MortgageDocs", backref="mortgage_document")
    employment_status = Column(String(20), nullable=False)
    annual_income = Column(Float, nullable=False)
    payback_period = Column(Integer, nullable=False)
    property_address = Column(String(20), nullable=False)
    property_value = Column(Float, nullable=False)
    down_payment = Column(Float, nullable=False)
    loan_type = Column(String(100), nullable=False, default="Mortgage")
    property_type = Column(String(20), nullable=False)