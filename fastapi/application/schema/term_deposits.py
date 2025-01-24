from pydantic import BaseModel
from datetime import datetime

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