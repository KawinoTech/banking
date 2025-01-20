from sqlalchemy import Column, String, Integer, ForeignKey, Float, Text, DateTime
from .base_model import BaseModel
from ..database import Base
from babel.numbers import format_currency
import random
import string

class Transaction(BaseModel):

    ref_no = Column(String(100), primary_key=True, unique=True)
    account = Column(String(50), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    remarks = Column(String(100), nullable=True, default="transact")
    beneficiary = Column(String(20), nullable=False)
    date_posted = Column(DateTime, nullable=False)

    def truncate_uuid(self):
        uuid = self.account
        parts = uuid.split('-')
    
        # Check if the UUID has the correct structure
        
        # Construct the truncated string
        truncated = f"{parts[0]}-***-{parts[-1][-2:]}"
        self.account = truncated
    
    def format_cash(self):
        self.amount = format_currency(self.amount, 'USD', locale='en_US')

    def truncate_datetime(self, format: str = "%Y-%m-%d %H:%M:%S"):
        date_posted = self.date_posted.strftime(format)
        self.date_posted = date_posted

    def generate_ref_number(self):
        part1 = ''.join(random.choices(string.ascii_uppercase, k=3))  # Three uppercase letters
        part2 = str(random.randint(0, 9))                            # One digit
        part3 = ''.join(random.choices(string.ascii_uppercase, k=3))  # Three uppercase letters
        part4 = str(random.randint(0, 9))                            # One digit
        part5 = ''.join(random.choices(string.ascii_uppercase, k=2))  # Two uppercase letters
        
        self.ref_no = f"{part1}{part2}{part3}{part4}{part5}"


class Transfer(Transaction, Base):

    __tablename__ = "transfer"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    transaction_type = Column(String(20), nullable=False, default="c2b_transfer") 

    

class PayBill(Transaction, Base):

    __tablename__ = "bill_payments"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    account_no = Column(String(100), nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    transaction_type = Column(String(20), nullable=False, default="paybill")


class BuyGoods(Transaction, Base):

    __tablename__ = "buy_goods_and_services"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    transaction_type = Column(String(23), nullable=False, default="buy_goods_and_services")

class Airtime(Transaction, Base):
    __tablename__ = "airtime"
    transaction_type = Column(String(23), nullable=False, default="airtime")
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))

