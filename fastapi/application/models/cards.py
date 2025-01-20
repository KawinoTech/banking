from sqlalchemy import Column, String, Integer, ForeignKey, Float, Text, DateTime
from .base_model import BaseModel
from ..database import Base
from sqlalchemy.orm import relationship
import random
import string


class BaseCards(BaseModel):
    full_name = Column(String(70), nullable=False)
    email_address = Column(String(30), nullable=False)
    phone = Column(String(11), nullable=False)
    date_issued = Column(DateTime, nullable=False)
    status = Column(String(10), nullable=False, default="Inactive")
    expiry_date = Column(DateTime, nullable=False)
    currency = Column(String(4), nullable=False, default='KES')
    delivery_option = Column(String(20), nullable=False)
    loyalty_point = Column(Float, nullable=False, default=1.0)
    card_no = Column(String(17), primary_key=True)
    

    @staticmethod
    def generate_card_no():
        random_16_digit = ''.join(random.choices(string.digits, k=16))
        return random_16_digit

    def reformat_card_no(self):
    # Format the number
        self.card_no = '-'.join(self.card_no[i:i+4] for i in range(0, 16, 4))
    
    def truncate_uuid(self):
        uuid = self.account_attached_no
        parts = uuid.split('-')
    
        # Check if the UUID has the correct structure
        
        # Construct the truncated string
        truncated = f"{parts[0]}-***-{parts[-1][-2:]}"
        self.account_attached_no = truncated
    def truncate_datetime(self, format: str = "%Y-%m-%d %H:%M:%S"):
        issue = self.date_issued.strftime(format).split(' ')[0]
        expiry = self.expiry_date.strftime(format).split(' ')[0]
        self.expiry_date = expiry
        self.date_issued = issue


class PrepaidCards(BaseCards, Base):
    __tablename__ = "prepaid_cards"
    card_type = Column(String(8), nullable=False, default="prepaid")
    balance = Column(Integer, nullable=False, default=50000)
    intended_usage = Column(Text, nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'), nullable=False)

class CreditCards(BaseCards, Base):
    __tablename__ = "credit_cards"
    card_type = Column(String(7), nullable=False, default="credit")
    balance = Column(Integer, nullable=False, default=0)
    due_date = Column(DateTime, nullable=False)
    annual_income = Column(Integer, nullable=True)
    employment_status = Column(String(20), nullable=True)
    rate = Column(Float, nullable=False, default=3.2)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    limit = Column(String(20), nullable=False, default="Not Assigned")
    card_classification = Column(String(20), nullable=False)

class DebitCards(BaseCards, Base):
    __tablename__ = "debit_cards"
    
    # Primary key for debit cards
    card_no = Column(String(17), primary_key=True)  # Assuming card_no is the primary key
    card_type = Column(String(5), nullable=False, default="debit")
    
    # Foreign key pointing to a personal account; one card belongs to one personal account
    account_attached_no = Column(String(50), ForeignKey('personal_accounts.account_no'), nullable=True)
    
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    card_classification = Column(String(20), nullable=False)