from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from ..database import Base
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from .transactions import PayBill, BuyGoods, Transfer
from .accounts import PersonalAccounts
from .loans import Loan
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
    Class User used to create user objects.l

    """

    full_name = Column(String(60), nullable=False)
    password_hash = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False, unique=True)



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
    
    def get_c2b_transactions(self, db):
        return db.query(Transfer).filter_by(owner_customer_no=self.customer_no).all()

    def get_bills(self, db):
        return db.query(PayBill).filter_by(owner_customer_no=self.customer_no).all()
    def get_amount(self, db):
        return db.query(BuyGoods).filter_by(owner_customer_no=self.customer_no).all()

class Customer(User, Base):
    __tablename__ = "customers"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    pin = Column(String(60), nullable=False)
    customer_no = Column(Integer, nullable=False, unique=True, index=True)
    bills = relationship("PayBill", backref="bill_payer")
    goods_payed = relationship("BuyGoods", backref="buyer")
    c2b_transfers = relationship("Transfer", backref="source")
    personal_accounts = relationship("PersonalAccounts", backref="owner")
    loans = relationship("Loan", backref="loaned_party")
    deposits = relationship("TermDeposit", backref="depositer")
    help_requests = relationship("ClientHelpRequest", backref="requester")
    client_reports = relationship("ClientReports", backref="reporter")
    prepaid_cards = relationship("PrepaidCards", backref="prepaid_card_wner")
    debit_cards = relationship("DebitCards", backref="debit_card_owner")
    credit_cards = relationship("CreditCards", backref="credit_card_owner")
    credit_score = Column(Float, nullable=False, default=0.00)
    relationship_managers = relationship(
        "RelationshipManager",
        secondary=customer_rm_association,
        back_populates="customers",
    )

class RelationshipManager(User, Base):
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