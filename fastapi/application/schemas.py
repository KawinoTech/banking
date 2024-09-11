from pydantic import BaseModel
from datetime import datetime
class User(BaseModel):
    pin : str
    password_hash : str 
    email : str
    customer_no: int

    class Config:
        from_attributes = True
class ResponseUser(User):
    id : str

class Transaction(BaseModel):
    account : str
    amount : int
    remarks : str


class Transfer(Transaction):
    beneficiary: str
class PayBill(Transaction):
    account_no: str
    bus_no: str

class BuyGoods(Transaction):
    store_no: str

class Account(BaseModel):
    account_type : str
    id_no : str
    kra_pin : str
    nationality : str
    currency : str
    account_name : str
    address : str
    telephone : str
    next_of_kin : str

class ResponseTransfer(Transfer):
    id : str

class ResponseAccount(BaseModel):
    account_name : str
class LoginUser(BaseModel):
    customer_no: int
    password_hash: str
class TokenData(BaseModel):
    customer_no: int
class ResponseAccount1(Account):
    account_no : str
    account_balance: int