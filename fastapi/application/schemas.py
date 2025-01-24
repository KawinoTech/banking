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



class LoginUser(BaseModel):
    customer_no: int
    password_hash: str
class TokenData(BaseModel):
    customer_no: int



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

