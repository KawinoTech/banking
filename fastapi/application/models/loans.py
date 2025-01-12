from ..database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from .base_model import BaseModel


class Loan(BaseModel, Base):
    __tablename__ = "loans"
    account_no = Column(String(100), primary_key=True)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    payback_period = Column(Integer, nullable=False)
    rate = Column(Float, nullable=False)
    account_balance = Column(Integer, nullable=False)
    account_type = Column(String(100), nullable=False)
    currency = Column(String(10), nullable=False)
    account_status = Column(String(8), nullable=False, default="open")