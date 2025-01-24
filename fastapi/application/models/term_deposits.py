from .base_model import BaseModel
from ..database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime
from babel.numbers import format_currency
from datetime import datetime

class TermDeposit(BaseModel, Base):
    """
    The TermDeposit class represents a term deposit in the system.

    Attributes:
        account_no (str): The unique identifier (UUID) for the term deposit account.
        account (str): The account number associated with the term deposit.
        owner_customer_no (int): The customer number of the owner of the term deposit (Foreign Key to Customers).
        status (str): The status of the term deposit (e.g., 'active', 'liquidated').
        maturity_period (int): The duration of the term deposit in months.
        maturity_date (datetime): The maturity date of the term deposit.
        rate (float): The interest rate for the term deposit.
        amount (int): The amount of money deposited in the term deposit.

    Methods:
        truncate_uuid(self): Truncates the account number UUID for privacy purposes.
        format_cash(self): Formats the deposit amount as a currency string.
        truncate_datetime(self, format: str): Truncates the maturity date to a specified string format.
        days_remaining(self): Calculates the days and hours remaining until the maturity date.
    """

    __tablename__ = "term_deposits"

    # Column definitions for the TermDeposit table
    account_no = Column(String(100), primary_key=True)
    account = Column(String(50), nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    status = Column(String(15), nullable=False, default="active")
    maturity_period = Column(Integer, nullable=False)
    maturity_date = Column(DateTime, nullable=False)
    rate = Column(Float, nullable=False, default=4.453)
    interest = Column(Float, nullable=False, default=0.00)
    accumulated_value = Column(Float, nullable=False)
    amount = Column(Integer, nullable=False)

    def truncate_uuid(self):
        """
        Truncates the account number (UUID) to a shorter format for privacy or display purposes.

        Example:
            Original UUID: "1234-abc-5678"
            Truncated UUID: "1234-***-78"
        """
        uuid = self.account_no
        parts = uuid.split('-')
    
        # Construct the truncated account number
        truncated = f"{parts[0]}-***-{parts[-1][-2:]}"
        self.account_no = truncated
    
    def format_cash(self):
        """
        Formats the term deposit amount as a currency string (USD).

        Example:
            Original amount: 5000
            Formatted amount: "$5,000.00"
        """
        self.amount = format_currency(self.amount, 'USD', locale='en_US')

    def truncate_datetime(self, format: str = "%Y-%m-%d %H:%M:%S"):
        """
        Truncates the maturity date to a specific string format.

        Parameters:
            format (str): The string format for the datetime. Default is "%Y-%m-%d %H:%M:%S".
        
        Example:
            Original datetime: datetime(2025, 12, 31, 12, 30)
            Truncated datetime: "2025-12-31 12:30:00"
        """
        date_posted = self.maturity_date.strftime(format)
        self.maturity_date = date_posted

    def days_remaining(self):
        """
        Calculates and sets the number of days and hours remaining until the maturity date.

        Example:
            Maturity Date: 2025-12-31 12:00:00
            Remaining time: "365 days 12 hours"
        """
        days_to_maturity = datetime.strptime(self.maturity_date, "%Y-%m-%d %H:%M:%S") - datetime.now()
        days = days_to_maturity.days
        hours = days_to_maturity.seconds // 3600
        setattr(self, "days_to_expiry", f"{days} days {hours} hours")
    
    def __repr__(self):
        return f"Owner: {self.owner_customer_no}, Current Value: Ksh {self.accumulated_value} Interest: Ksh{self.interest}"
