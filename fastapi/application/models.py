from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text, DateTime, Float
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from uuid import uuid4
import random
import string

bycrypt = Bcrypt()


class User(Base):
    """
    Class User used to create user objects.

    """
    __tablename__ = "user"
    id = Column(String(100), primary_key=True, default=str(uuid4()))
    password_hash = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    pin = Column(String(60), nullable=False, unique=True)
    customer_no = Column(Integer, nullable=False, unique=True)
    bills = relationship("PayBill", backref="bill_payer")
    goods_payed = relationship("BuyGoods", backref="buyer")
    c2b_transfers = relationship("Transfer", backref="source")
    accounts = relationship("Account", backref="owner")
    loans = relationship("Loan", backref="loaned_party")
    deposits = relationship("TermDeposit", backref="depositer")
    help_requests = relationship("ClientHelpRequest", backref="requester")
    client_reports = relationship("ClientReports", backref="reporter")
    prepaid_cards = relationship("PrepaidCards", backref="prepaid_card_wner")
    debit_cards = relationship("DebitCards", backref="debit_card_owner")
    credit_cards = relationship("CreditCards", backref="credit_card_owner")
    credit_score = Column(Float, nullable=False, default=0.00)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bycrypt.generate_password_hash(plain_text_password).decode('utf-8')
        return self.password_hash
    
    def check_password(self, attempted_pasword):
        #Returns Boolean
        return self.password_hash == attempted_pasword

class Transfer(Base):

    __tablename__ = "transfer"
    id = Column(String(100), nullable=False)
    account = Column(String(50), nullable=False)
    amount = Column(Integer, nullable=False)
    remarks = Column(String(100), nullable=False)
    beneficiary = Column(Text, nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow())
    ref_no = Column(String(100), primary_key=True)
    owner_customer_no = Column(Integer, ForeignKey('user.customer_no'))

    

class PayBill(Base):

    __tablename__ = "bill_payments"
    id = Column(String(100), primary_key=True, nullable=False)
    account = Column(String(100), nullable=False)
    amount = Column(Integer, nullable=False)
    remarks = Column(Text, nullable=False)
    bus_no = Column(String(100), nullable=False)
    account_no = Column(String(100), nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow())
    ref_no = Column(String(100), nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('user.customer_no'))

class BuyGoods(Base):

    __tablename__ = "buy_goods_and_services"
    id = Column(String(100), primary_key=True)
    account = Column(String(100), nullable=False)
    amount = Column(Integer, nullable=False)
    remarks = Column(Text, nullable=False)
    store_no = Column(String(100), nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow())
    ref_no = Column(String(100), nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('user.customer_no'))

class Loan(Base):
    __tablename__ = "loans"
    account_no = Column(String(100), primary_key=True)
    date_posted = Column(DateTime, nullable=False, default=datetime.now())
    owner_customer_no = Column(Integer, ForeignKey('user.customer_no'))
    payback_period = Column(Integer, nullable=False)
    rate = Column(Float, nullable=False)
    account_balance = Column(Integer, nullable=False)
    account_type = Column(String(100), nullable=False)
    currency = Column(String(10), nullable=False)
    account_status = Column(String(8), nullable=False, default="open")

class TermDeposit(Base):
    __tablename__ = "term_deposits"
    account_no = Column(String(100), primary_key=True)
    date_posted = Column(DateTime, nullable=False, default=datetime.now())
    owner_customer_no = Column(Integer, ForeignKey('user.customer_no'))
    maturity_period = Column(Integer, nullable=False)
    rate = Column(Float, nullable=False)
    account_balance = Column(Integer, nullable=False)
    account_type = Column(String(100), nullable=False)
    currency = Column(String(10), nullable=False)

class ClientHelpRequest(Base):
    __tablename__ = "client_help"
    id = Column(String(100), primary_key=True)
    date_posted = Column(DateTime, nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('user.customer_no'))
    text = Column(Text, nullable=False)
    status_resolved = Column(Boolean, nullable=False, default=False)

class ClientReports(Base):
    __tablename__ = "client_reports"
    id = Column(String(100), primary_key=True)
    date_posted = Column(DateTime, nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('user.customer_no'))
    text = Column(Text, nullable=False)
    status_resolved = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"{self.id}"
    
class BaseCards():
    full_name = Column(String(70), nullable=False)
    email_address = Column(String(30), nullable=False)
    phone = Column(String(11), nullable=False)
    id = Column(String(100), primary_key=True)
    date_requested = Column(DateTime, nullable=False)
    date_issued = Column(DateTime, nullable=False)
    status = Column(String(10), nullable=False, default="inactive")
    expiry_date = Column(DateTime, nullable=False)
    currency = Column(String(4), nullable=False, default='KES')
    delivery_option = Column(String(20), nullable=False)
    loyalty_point = Column(Float, nullable=False, default=1.0)
    card_no = Column(String(11), primary_key=True)

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
    card_type = Column(String(5), nullable=False, default="prepaid")
    balance = Column(Integer, nullable=False, default=50000)
    due_date = Column(DateTime, nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('user.customer_no'))

class CreditCards(BaseCards, Base):
    __tablename__ = "credit_cards"
    card_type = Column(String(5), nullable=False, default="credit")
    balance = Column(Integer, nullable=False, default=-50000)
    due_date = Column(DateTime, nullable=False)
    rate = Column(Float, nullable=False, default=3.2)
    owner_customer_no = Column(Integer, ForeignKey('user.customer_no'))
class DebitCards(BaseCards, Base):
    __tablename__ = "debit_cards"
    
    # Add card_no as primary key or unique constraint to ensure one-to-one
    card_no = Column(String(17), primary_key=True)  # Assuming card_no is the primary key
    card_type = Column(String(5), nullable=False, default="debit")
    card_classification = Column(String(20), nullable=False)
    
    # Define relationship with Account, ensuring it's one-to-one
    account_attached_no = Column(String(37), ForeignKey('accounts.account_no'), nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('user.customer_no'))

class Account(Base):
    __tablename__ = "accounts"
    
    account_no = Column(String(100), primary_key=True)
    date_posted = Column(DateTime, nullable=False, default=datetime.now())
    id_no = Column(String(10), nullable=False)
    kra_pin = Column(String(10), nullable=False)
    nationality = Column(String(10), nullable=False)
    account_type = Column(String(100), nullable=False)
    currency = Column(String(10), nullable=False)
    account_name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    telephone = Column(String(10), nullable=False)
    next_of_kin = Column(String(100), nullable=False)
    account_balance = Column(Integer, nullable=False, default=50000)
    owner_customer_no = Column(Integer, ForeignKey('user.customer_no'))
    overdraft = Column(Boolean, nullable=False, default=False)
    account_status = Column(String(8), nullable=False, default="open")
    
    # Foreign key linking to the DebitCards table
    debit_card_attached = relationship("DebitCards", backref="accounts", uselist=False)