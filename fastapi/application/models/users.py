"""
Module: users.py

This module defines the data models for managing user and customer-related information in a financial application. It integrates with SQLAlchemy for ORM support and uses Flask-Bcrypt for secure password hashing. Additionally, it defines many-to-many relationships for customers and relationship managers.

Classes:
1. **User**:
    - The base class for user-related data.
    - Contains attributes and methods for authentication, including password hashing and transaction retrieval.

2. **Customer**:
    - Inherits from `User` and `Base`.
    - Represents individual customers in the system.
    - Tracks various customer-specific data such as accounts, transactions, deposits, loans, credit scores, and help requests.

3. **RelationshipManager**:
    - Inherits from `User` and `Base`.
    - Represents relationship managers who oversee multiple customers.
    - Includes attributes specific to the manager, such as department and employee ID.

Tables:
1. **customer_rm_association**:
    - Defines a many-to-many association table between customers and relationship managers.

Dependencies:
- `sqlalchemy`: Used for defining models and relationships.
- `flask_bcrypt`: Provides secure password hashing for user authentication.
- Other modules include:
    - `PayBill`, `BuyGoods`, `Transfer`, `Airtime`, `TopUpWallet` (transaction types).
    - `PersonalAccounts`, `CorporateAccounts` (account types).
    - `PersonalLoans`, `TermDeposit` (loans and deposits).
    - `ClientHelpRequest`, `ClientReports` (customer service)."""

from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from . import Base
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from .transactions import PayBill, BuyGoods, Transfer, Airtime, TopUpWallet
from .accounts import PersonalAccounts, CorporateAccounts
from .loans import PersonalLoans
from .term_deposits import TermDeposit
from .customer_service import ClientHelpRequest, ClientReports
from flask_bcrypt import Bcrypt

bycrypt = Bcrypt()

customer_rm_association = Table(
    "customer_rm_association",
    Base.metadata,
    Column("customer_no", Integer, ForeignKey("customers.customer_no"), primary_key=True),
    Column("relationship_manager_id", String(20), ForeignKey("relationship_managers.employee_id"), primary_key=True),
)

class User(BaseModel):
    """
    Represents a general user in the system.

    **Attributes**:
    - `full_name (str)`: The full name of the user.
    - `password_hash (str)`: The hashed password of the user (stored securely).
    - `email (str)`: The email address of the user (must be unique).

    **Properties**:
    - `password`: A property for setting and securely hashing the user's password.

    """

    full_name = Column(String(60), nullable=False)
    password_hash = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False, unique=True)



    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        #Hashes a plain-text password and stores it in `password_hash`
        self.password_hash = bycrypt.generate_password_hash(plain_text_password).decode('utf-8')
        return self.password_hash
    
    def check_password(self, attempted_pasword):
        #Returns Boolean
        return self.password_hash == attempted_pasword
    
    """
    - `get_c2b_transactions(db)`: Retrieves customer-to-business transfers for the user.
    - `get_bills(db)`: Retrieves bill payment transactions for the user.
    - `get_amount(db)`: Retrieves goods purchase transactions for the user.
    - `get_airtime(db)`: Retrieves airtime purchase transactions for the user.
    - `get_topups(db)`: Retrieves wallet top-up transactions for the user.
    """
    
    def get_c2b_transactions(self, db):
        return db.query(Transfer).filter_by(owner_customer_no=self.customer_no).all()

    def get_bills(self, db):
        return db.query(PayBill).filter_by(owner_customer_no=self.customer_no).all()
    def get_amount(self, db):
        return db.query(BuyGoods).filter_by(owner_customer_no=self.customer_no).all()
    def get_airtime(self, db):
        return db.query(Airtime).filter_by(owner_customer_no=self.customer_no).all()
    def get_topups(self, db):
        return db.query(TopUpWallet).filter_by(owner_customer_no=self.customer_no).all()

class Customer(User, Base):
    """
    Extends the `User` model to include customer-specific information.

**Attributes**:
- `pin (str)`: The customer's unique PIN for secure access.
- `customer_no (int)`: A unique customer identifier (indexed for performance).
- `credit_score (float)`: A numeric representation of the customer's creditworthiness.
- Relationships:
  - `bills`: Links to bill payment transactions.
  - `airtime`: Links to airtime transactions.
  - `goods_payed`: Links to goods purchase transactions.
  - `c2b_transfers`: Links to customer-to-business transfers.
  - `topups`: Links to wallet top-ups.
  - `personal_accounts`: Links to personal accounts.
  - `corporate_accounts`: Links to corporate accounts.
  - `deposits`: Links to term deposits.
  - `help_requests`: Links to client help requests.
  - `client_reports`: Links to client reports.
  - `prepaid_cards`, `debit_cards`, `credit_cards`: Links to different types of cards.
  - `personal_loans`: Links to personal loans.
  - `relationship_managers`: Many-to-many relationship with relationship managers.
    """
    __tablename__ = "customers"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    pin = Column(String(60), nullable=False)
    customer_no = Column(Integer, nullable=False, unique=True, index=True)
    bills = relationship("PayBill", backref="bill_payer")
    airtime = relationship("Airtime", backref="sender")
    goods_payed = relationship("BuyGoods", backref="buyer")
    c2b_transfers = relationship("Transfer", backref="source")
    topups = relationship("TopUpWallet", backref="source")
    personal_accounts = relationship("PersonalAccounts", backref="owner")
    corporate_accounts = relationship("CorporateAccounts", backref="owner")
    deposits = relationship("TermDeposit", backref="depositer")
    help_requests = relationship("ClientHelpRequest", backref="requester")
    client_reports = relationship("ClientReports", backref="reporter")
    prepaid_cards = relationship("PrepaidCards", backref="prepaid_card_wner")
    debit_cards = relationship("DebitCards", backref="debit_card_owner")
    credit_cards = relationship("CreditCards", backref="credit_card_owner")
    personal_loans = relationship("PersonalLoans", backref="lendee")
    credit_score = Column(Float, nullable=False, default=0.00)
    relationship_managers = relationship(
        "RelationshipManager",
        secondary=customer_rm_association,
        back_populates="customers",
    )

class RelationshipManager(User, Base):
    """
    Extends the `User` model to include data for managing customer relationships.

**Attributes**:
- `department (str)`: The department where the manager works.
- `employee_id (str)`: A unique identifier for the manager (indexed for performance).
- `customers`: Many-to-many relationship linking to customers.

---

### 4. customer_rm_association
A many-to-many association table connecting customers and relationship managers.

**Columns**:
- `customer_no (int)`: Foreign key linking to the `customers` table.
- `relationship_manager_id (str)`: Foreign key linking to the `relationship_managers` table
    """
    __tablename__ = "relationship_managers"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    department = Column(String(20), nullable=False)
    employee_id = Column(String(20), nullable=False, unique=True, index=True)
    customers = relationship(
        "Customer",
        secondary=customer_rm_association,
        back_populates="relationship_managers",
    )