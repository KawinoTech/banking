from .base_model import BaseModel
from ..database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime
from babel.numbers import format_currency
from datetime import datetime

class TermDeposit(BaseModel, Base):

    __tablename__ = "term_deposits"
    account_no = Column(String(100), primary_key=True)
    account = Column(String(50), nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    status = Column(String(15), nullable=False, default="active")
    maturity_period = Column(Integer, nullable=False)
    maturity_date = Column(DateTime, nullable=False)
    rate = Column(Float, nullable=False, default=4.453)
    amount = Column(Integer, nullable=False)

    def truncate_uuid(self):
        uuid = self.account_no
        parts = uuid.split('-')
    
        # Check if the UUID has the correct structure
        
        # Construct the truncated string
        truncated = f"{parts[0]}-***-{parts[-1][-2:]}"
        self.account_no = truncated
    
    def format_cash(self):
        self.amount = format_currency(self.amount, 'USD', locale='en_US')

    def truncate_datetime(self, format: str = "%Y-%m-%d %H:%M:%S"):
        date_posted = self.maturity_date.strftime(format)
        self.maturity_date = date_posted
    def days_remaining(self):
        days_to_maturity = datetime.strptime(self.maturity_date, "%Y-%m-%d %H:%M:%S") - datetime.now()
        days = days_to_maturity.days
        hours = days_to_maturity.seconds // 3600
        setattr(self, "days_to_expiry", f"{days} days {hours} hours")