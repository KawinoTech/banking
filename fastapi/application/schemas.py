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
    payload: dict
    signature: str
class HelpDesk(BaseModel):
    text : str
class Report(BaseModel):
    text : str


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

class ResponseTransact(BaseModel):
    ref_no: str

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

class ResponseHelp(BaseModel):
    id : str
class ReportResponse(BaseModel):
    id : str

class CardApplication(BaseModel):
    payload: dict
    signature: str

class CardApplicationResponse(BaseModel):
    full_name: str
    email_address: str
    phone: str
    card_type: str
    delivery_option: str
    card_classification: str
    card_no: str
    account_attached_no: str
    status: str
    date_issued: datetime
    expiry_date: datetime

class GetDebitCards(BaseModel):
    full_name: str
    card_type: str
    card_classification: str
    card_no: str
    account_attached_no: str
    status: str
    date_issued: str
    expiry_date: str
