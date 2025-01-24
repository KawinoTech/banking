from datetime import datetime
from datetime import timedelta
from fastapi import  UploadFile
from typing import List
from pydantic import BaseModel, EmailStr, Field
class User(BaseModel):
    full_name: str
    pin : str
    password_hash : str 
    email : str
    customer_no: int

    class Config:
        from_attributes = True
class ResponseUser(BaseModel):
    full_name: str
    id : str

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

class ResponseAccount(BaseModel):
    account_name: str
class LoginUser(BaseModel):
    customer_no: int
    password_hash: str
class TokenData(BaseModel):
    customer_no: int

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

class PersonalLoanApplication(BaseModel):
    payload: dict
    signature: str
class LoanSummary(BaseModel):
    amount: int
    account_no: str
    payback_period: int
    purpose: str
    outstanding_amount: float
    loan_type: str
    accrued_interest: float
    principal_paid: float

class BusinessLoanApplication(BaseModel):
    id_no: str
    purpose: str
    payback_period: int
    account_name: str
    address: str
    pmargin: float
    dob: str
    annual_income: float
    amount: float

class Mortgage(BaseModel):
    account_name: str
    employment_status: str
    annual_income: float
    payback_period: int
    property_address: str
    property_value: float
    down_payment: float
    amount: float
    property_type: str
    rate: int

class AllTransactions(BaseModel):
    account: str
    amount: str
    ref_no: str
    transaction_type: str
    beneficiary: str
    date_posted: str

class BookTD(BaseModel):
    payload: dict
    signature: str

class TDSummary(BaseModel):
    account_no: str
    rate: float
    amount: int
    maturity_date: datetime
class ChildTDSummary(TDSummary):
    account_no: str
    rate: float
    amount: str
    maturity_date: str
    days_to_expiry: str

class Liquidate(BaseModel):
    payload: dict
    signature: str
'''
class SignatoryResponse(BaseModel):
    name: str
    id_no: str
    file_name: str


class Signatory(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Name of the signatory")
    id_no: str = Field(..., min_length=6, max_length=11, description="National ID or Passport number")

class SignatoryInput(BaseModel):
    names: List[str] = Field(..., description="Names of the signatories")
    id_nos: List[str] = Field(..., description="National ID numbers of the signatories")
    account_type: List[str] = Field(..., description="Type of the accounts")
    account_name: List[str] = Field(..., description="Names of the accounts")
    currency: List[str] = Field(..., description="Currency preferences")
    address: List[str] = Field(..., description="Premise addresses")
    kra_pin: List[str] = Field(..., description="KRA PINs for the signatories")
    telephone: List[str] = Field(..., description="Telephone numbers of the signatories")
    email: List[EmailStr] = Field(..., description="Email addresses of the signatories")
    dob: List[str] = Field(..., description="Date of birth of the signatories")
    source_of_funds: List[str] = Field(..., description="Sources of funds")
    annual_income: List[str] = Field(..., description="Annual income levels")
    intended_usage: List[str] = Field(..., description="Intended usage of the accounts")


class FileUploads(BaseModel):
    files: List[UploadFile] = Field(..., description="Uploaded files (general documents)")
    tax_cert: List[UploadFile] = Field(..., description="Tax compliance certificates")
    reg_cert: List[UploadFile] = Field(..., description="Registration certificates")
    passport: List[UploadFile] = Field(..., description="Passport scans or images")


class CorporateAccountInput(SignatoryInput, FileUploads):
    """
    This model extends both SignatoryInput and FileUploads 
    to encapsulate all the required fields for creating a corporate account.
    """
    pass



'''

