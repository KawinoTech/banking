from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Float, Text, DateTime
from .base_model import BaseModel
from .cards import DebitCards
from .files import Signatory, CorporateDocs, PersonalDocs, F_C_A_Docs
from ..database import Base
from babel.numbers import format_currency
from sqlalchemy.orm import relationship
from datetime import datetime

class Account(BaseModel):

    account_no = Column(String(36), primary_key=True, index=True, unique=True)
    id_no = Column(String(10), nullable=False)
    currency = Column(String(3), nullable=False, default="KES")
    kra_pin = Column(String(15), nullable=False)
    nationality = Column(String(10), nullable=False)
    account_type = Column(String(15), nullable=False)
    account_name = Column(String(50), nullable=False)
    address = Column(String(30), nullable=False)
    telephone = Column(String(15), nullable=False)
    account_balance = Column(Float, nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    account_status = Column(String(8), nullable=False, default="pending")
    email = Column(String(25), nullable=False)
    dob = Column(DateTime, nullable=False)
    annual_income = Column(Integer, nullable=False)
    source_of_funds = Column(Text, nullable=False)
    intended_usage = Column(Text, nullable=False)

    def truncate_uuid(self):
        uuid = self.account_no
        parts = uuid.split('-')
    
        # Check if the UUID has the correct structure
        
        # Construct the truncated string
        truncated = f"{parts[0]}-***-{parts[-1][-2:]}"
        self.account_no = truncated
    def format_cash(self):
        self.account_balance = format_currency(self.account_balance, 'USD', locale='en_US')

class PersonalAccounts(Account, Base):
    __tablename__ = "personal_accounts"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    nssf_no = Column(String(15), nullable=False)
    nok_relationship = Column(String(9), nullable=False)
    next_of_kin = Column(String(30), nullable=False)
    next_of_kin_id = Column(String(10), nullable=False)
    overdraft = Column(Boolean, nullable=False, default=False)
    employment_status = Column(String(13), nullable=False)
    
    # Reverse relationship: A personal account can have multiple debit cards
    debit_cards = relationship("DebitCards", backref="personal_account")
    
    personal_documents = relationship("PersonalDocs", backref="personal_account")


class CorporateAccounts(Account, Base):
    __tablename__ = "corporate_accounts"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dob =  datetime.strptime(self.dob, "%Y-%m-%d")

    overdraft = Column(Boolean, nullable=False, default=False)
    debit_card_no = Column(String(17), ForeignKey('debit_cards.card_no'))
    signatures = relationship("Signatory", backref="signatory")
    corporate_documents = relationship("CorporateDocs", backref="corporate_account")


class ForeignCurrency(Account, Base):
    _sellPound = 140.45
    _sellEuro = 132.45
    _sellUSD = 129.40

    __tablename__ = "foreign_currency_accounts"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account_balance = 50000.00
    next_of_kin = Column(String(30), nullable=False)
    next_of_kin_id = Column(String(10), nullable=False)
    nok_relationship = Column(String(9), nullable=False)
    equivalent_balance = Column(Float, nullable=False)
    fc_account_documents = relationship("F_C_A_Docs", backref="foreign_currency_account")

    def update_balance(self):
        if self.currency == "USD":
            self.equivalent_balance = self.account_balance * self._sellUSD
        if self.currency == "EUR":
            self.equivalent_balance = self.account_balance * self._sellEuro
        if self.currency == "POUND":
            self.equivalent_balance = self.account_balance * self._sellPound

