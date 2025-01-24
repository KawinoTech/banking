from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Float, Text, DateTime
from .base_model import BaseModel
from .cards import DebitCards
from .files import Signatory, CorporateDocs, PersonalDocs, F_C_A_Docs
from ..database import Base
from babel.numbers import format_currency
from sqlalchemy.orm import relationship
from datetime import datetime

### Base Account Model ###
class Account(BaseModel):
    """
    Represents a general account with shared attributes and methods for all account types.

    Attributes:
        - account_no (str): Unique account number (primary key).
        - id_no (str): National ID number of the account owner.
        - currency (str): The currency of the account (default is "KES").
        - kra_pin (str): KRA PIN (Kenya Revenue Authority Personal Identification Number).
        - nationality (str): Nationality of the account holder.
        - account_type (str): Type of account (e.g., Savings, Current).
        - account_name (str): Name on the account.
        - address (str): Residential address of the account holder.
        - telephone (str): Contact telephone number.
        - account_balance (float): Current balance in the account.
        - owner_customer_no (int): Foreign key referencing the customer number.
        - account_status (str): Current status of the account (default is "pending").
        - email (str): Email address associated with the account.
        - dob (datetime): Date of birth of the account holder.
        - annual_income (int): Declared annual income of the account holder.
        - source_of_funds (str): Source of the funds in the account.
        - intended_usage (str): Description of how the account will be used.
    """
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
        """
        Truncates the UUID to a shorter, anonymized format.

        Example:
            Input: "123e4567-e89b-12d3-a456-426614174000"
            Output: "123e4567-***-00"
        """
        uuid = self.account_no
        parts = uuid.split('-')
        truncated = f"{parts[0]}-***-{parts[-1][-2:]}"
        self.account_no = truncated

    def format_cash(self):
        """
        Formats the account balance into a readable currency string (USD).
        """
        self.account_balance = format_currency(self.account_balance, 'USD', locale='en_US')


### Personal Accounts ###
class PersonalAccounts(Account, Base):
    """
    Represents a personal account inheriting from the base Account model.

    Additional Attributes:
        - nssf_no (str): NSSF (National Social Security Fund) number.
        - nok_relationship (str): Relationship of the next of kin to the account holder.
        - next_of_kin (str): Name of the next of kin.
        - next_of_kin_id (str): ID number of the next of kin.
        - overdraft (bool): Indicates if the account has an overdraft facility.
        - employment_status (str): Employment status of the account holder.
        - debit_cards (relationship): Associated debit cards for the account.
        - personal_documents (relationship): Related personal documents for the account.
    """
    __tablename__ = "personal_accounts"

    nssf_no = Column(String(15), nullable=False)
    nok_relationship = Column(String(9), nullable=False)
    next_of_kin = Column(String(30), nullable=False)
    next_of_kin_id = Column(String(10), nullable=False)
    overdraft = Column(Boolean, nullable=False, default=False)
    employment_status = Column(String(13), nullable=False)
    
    debit_cards = relationship("DebitCards", backref="personal_account")
    personal_documents = relationship("PersonalDocs", backref="personal_account")


### Corporate Accounts ###
class CorporateAccounts(Account, Base):
    """
    Represents a corporate account inheriting from the base Account model.

    Additional Attributes:
        - overdraft (bool): Indicates if the account has an overdraft facility.
        - debit_card_no (str): Foreign key linking to a debit card.
        - signatures (relationship): Associated signatories for the account.
        - corporate_documents (relationship): Related corporate documents for the account.
    """
    __tablename__ = "corporate_accounts"

    overdraft = Column(Boolean, nullable=False, default=False)
    debit_card_no = Column(String(17), ForeignKey('debit_cards.card_no'))
    signatures = relationship("Signatory", backref="signatory")
    corporate_documents = relationship("CorporateDocs", backref="corporate_account")

    def __init__(self, *args, **kwargs):
        """
        Custom initialization for `dob` to handle datetime conversion.
        """
        super().__init__(*args, **kwargs)
        if isinstance(self.dob, str):
            self.dob = datetime.strptime(self.dob, "%Y-%m-%d")


### Foreign Currency Accounts ###
class ForeignCurrency(Account, Base):
    """
    Represents a foreign currency account inheriting from the base Account model.

    Additional Attributes:
        - next_of_kin (str): Name of the next of kin.
        - next_of_kin_id (str): ID number of the next of kin.
        - nok_relationship (str): Relationship of the next of kin to the account holder.
        - equivalent_balance (float): Account balance converted to the local currency.
        - fc_account_documents (relationship): Related foreign currency account documents.
        - _sellPound, _sellEuro, _sellUSD: Conversion rates for currency.
    """
    __tablename__ = "foreign_currency_accounts"

    _sellPound = 140.45
    _sellEuro = 132.45
    _sellUSD = 129.40

    next_of_kin = Column(String(30), nullable=False)
    next_of_kin_id = Column(String(10), nullable=False)
    nok_relationship = Column(String(9), nullable=False)
    equivalent_balance = Column(Float, nullable=False)
    fc_account_documents = relationship("F_C_A_Docs", backref="foreign_currency_account")

    def update_balance(self):
        """
        Updates the equivalent balance based on the current currency conversion rate.
        """
        if self.currency == "USD":
            self.equivalent_balance = self.account_balance * self._sellUSD
        elif self.currency == "EUR":
            self.equivalent_balance = self.account_balance * self._sellEuro
        elif self.currency == "POUND":
            self.equivalent_balance = self.account_balance * self._sellPound

