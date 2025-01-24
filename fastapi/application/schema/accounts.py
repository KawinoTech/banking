from pydantic import BaseModel
class Account(BaseModel):
    account_type: str
    account_name: str
    id_no: str
    nationality: str
    kra_pin: str
    telephone: str
    email: str
    dob: str
    source_of_funds: str
    address: str
    annual_income: int
    intended_usage: str

class PersonalAccount(Account):
    nssf_no: str
    next_of_kin: str
    next_of_kin_id: str
    nok_relationship: str
    employment_status: str

class ForeignCurrencyAccount(Account):
    currency: str
    employment_status: str
    next_of_kin: str
    next_of_kin_id: str
    nok_relationship: str

class CorporateAccount(Account):
    pass

class ResponseAccount1(BaseModel):
    account_no : str
    account_balance: int
    account_type: str
    currency: str
class ResponseAccount2(BaseModel):
    account_no : str
    account_balance: str
    account_type: str
    currency: str

class ResponseAccount(BaseModel):
    account_name: str