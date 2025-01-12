from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Float, Text
from .base_model import BaseModel
from .cards import DebitCards
from ..database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Account(BaseModel):

    account_no = Column(String(36), primary_key=True, index=True, unique=True)
    id_no = Column(String(10), nullable=False)
    currency = Column(String(3), nullable=False, default="KES")
    kra_pin = Column(String(10), nullable=False)
    nationality = Column(String(10), nullable=False)
    account_type = Column(String(15), nullable=False)
    account_name = Column(String(30), nullable=False)
    address = Column(String(30), nullable=False)
    telephone = Column(String(13), nullable=False)
    next_of_kin = Column(String(30), nullable=False)
    next_of_kin_id = Column(String(10), nullable=False)
    account_balance = Column(Float, nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    account_status = Column(String(8), nullable=False, default="pending")
    email = Column(String(25), nullable=False)
    dob = Column(String(15), nullable=False)
    annual_income = Column(Integer, nullable=False)
    source_of_funds = Column(String(16), nullable=False)
    intended_usage = Column(Text, nullable=False)
    # Foreign key linking to the DebitCards table

class PersonalAccounts(Account, Base):
    __tablename__ = "personal_accounts"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    nssf_no = Column(String(15), nullable=False)
    relationship = Column(String(9), nullable=False)
    overdraft = Column(Boolean, nullable=False, default=False)
    employment_status = Column(String(13), nullable=False)
    debit_card_no = Column(String(17), ForeignKey('debit_cards.card_no'))


class CorporateAccounts(Account, Base):
    __tablename__ = "corporate_accounts"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dob =  datetime.strptime(self.dob, "%Y-%m-%d")

    overdraft = Column(Boolean, nullable=False, default=False)
    debit_card_no = Column(String(17), ForeignKey('debit_cards.card_no'))

class ForeignCurrency(Account, Base):
    __tablename__ = "foreign_currency_accounts"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account_balance = 50000.00
    equivalent_balance = Column(Float, nullable=False)

    def update_balance(self):
        card_rate = 129.40
        self.equivalent_balance = self.account_balance * card_rate

