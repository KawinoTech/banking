from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from uuid import uuid4
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


    #collaborating = relationship('Idea', secondary=user_idea, backref='collaborator')
    #pending_collaborating = relationship('Idea', secondary=pending_request, backref='requster')

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

class Account(Base):
    __tablename__ = "accounts"
    account_no = Column(String(100), primary_key=True)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow())
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
