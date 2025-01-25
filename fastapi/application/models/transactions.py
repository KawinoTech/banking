"""
Module: transactions.py

This module provides the implementation of transaction-related models used in a financial application.

Key Features:
- Models for different transaction types, including transfers, bill payments, airtime purchases, goods purchases, and wallet top-ups.
- Common functionality for handling transactions such as UUID truncation, currency formatting, and reference number generation.
- Seamless database integration with SQLAlchemy.

Classes:
1. **Transaction**:
    - Base model for financial transactions, containing common attributes such as reference number, account, amount, remarks, beneficiary, and date of the transaction.
    - Provides utility methods for data truncation and formatting.
    
2. **Transfer**:
    - Represents a transfer transaction.
    - Contains additional attributes such as the owner customer number and transaction type (defaults to "c2b_transfer").

3. **PayBill**:
    - Represents a bill payment transaction.
    - Adds attributes for customer ownership and transaction type (defaults to "paybill").

4. **BuyGoods**:
    - Represents a transaction for purchasing goods and services.
    - Includes attributes for customer ownership and transaction type (defaults to "buy_goods_and_services").

5. **Airtime**:
    - Represents an airtime purchase transaction.
    - Handles details specific to airtime purchases with transaction type set to "airtime".

6. **TopUpWallet**:
    - Represents a wallet top-up transaction.
    - Adds attributes for customer ownership, transaction type (defaults to "wallet_topup"), and service provider.

Dependencies:
- SQLAlchemy: ORM for database interactions.
- Babel: Formatting currency representations.
- random, string: Utility modules for generating unique reference numbers.
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime
from .base_model import BaseModel
from . import Base
from babel.numbers import format_currency
import random
import string


class Transaction(BaseModel):
    """
    Base model for financial transactions.
    
    This model stores the common attributes for all transaction types, including the
    account, amount, remarks, beneficiary, and date of transaction. It also provides
    utility methods for formatting data like UUID truncation, currency formatting, and
    datetime truncation.

    Attributes:
        ref_no (str): Unique reference number for the transaction.
        account (str): The account involved in the transaction.
        amount (float): The transaction amount.
        remarks (str): Optional remarks associated with the transaction.
        beneficiary (str): The beneficiary of the transaction.
        date_posted (datetime): The timestamp when the transaction occurred.
    """
    
    # Primary key and unique identifier for the transaction.
    ref_no = Column(String(100), primary_key=True, unique=True)
    account = Column(String(50), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    remarks = Column(String(100), nullable=True, default="transact")
    beneficiary = Column(String(20), nullable=False)
    date_posted = Column(DateTime, nullable=False)

    def truncate_uuid(self):
        """
        Truncates the account field (presumed to be a UUID) to hide the middle part.

        This method splits the UUID (assumed to be in string format) and replaces the middle
        section with asterisks ('***') for security or privacy reasons. It only retains the first
        part and the last two characters of the UUID.
        """
        uuid = self.account
        parts = uuid.split('-')
        
        # Construct the truncated string with first part and last 2 characters of last part
        truncated = f"{parts[0]}-***-{parts[-1][-2:]}"
        self.account = truncated
    
    def format_cash(self):
        """
        Formats the amount attribute into currency format.

        The `amount` is formatted as a currency using the US Dollar ('USD') format with 
        the `en_US` locale. This method sets the `amount` field to a formatted string representation.
        """
        self.amount = format_currency(self.amount, 'USD', locale='en_US')

    def truncate_datetime(self, format: str = "%Y-%m-%d %H:%M:%S"):
        """
        Truncates the `date_posted` timestamp to a specified string format.

        The method formats the `date_posted` attribute using the provided format.
        By default, it uses the format "%Y-%m-%d %H:%M:%S". This is typically used
        to format datetime objects into a human-readable string representation.

        Args:
            format (str): A format string in the `strftime` style.
        """
        date_posted = self.date_posted.strftime(format)
        self.date_posted = date_posted

    def generate_ref_number(self):
        """
        Generates a unique reference number for the transaction.

        This method constructs a reference number composed of random uppercase letters 
        and digits to ensure that it is both unique and hard to predict. The reference
        number follows a format: three uppercase letters, one digit, three uppercase 
        letters, one digit, and two uppercase letters.
        """
        part1 = ''.join(random.choices(string.ascii_uppercase, k=3))  # Three uppercase letters
        part2 = str(random.randint(0, 9))                            # One digit
        part3 = ''.join(random.choices(string.ascii_uppercase, k=3))  # Three uppercase letters
        part4 = str(random.randint(0, 9))                            # One digit
        part5 = ''.join(random.choices(string.ascii_uppercase, k=2))  # Two uppercase letters
        
        # Combines parts into a reference number
        self.ref_no = f"{part1}{part2}{part3}{part4}{part5}"


class Transfer(Transaction, Base):
    """
    Represents a transfer transaction.

    This model extends the `Transaction` model and provides additional attributes 
    and behavior specific to a transfer transaction. It stores details such as the 
    owner of the account and the transaction type (defaults to "c2b_transfer").
    
    Attributes:
        owner_customer_no (int): The foreign key to the `customers` table (owner of the account).
        transaction_type (str): The type of transaction (default is "c2b_transfer").
    """

    __tablename__ = "transfer"

    # Inherit from Transaction for base attributes

    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))  # Foreign key referencing Customer
    transaction_type = Column(String(20), nullable=False, default="c2b_transfer")  # Transaction type field

    def __init__(self, *args, **kwargs):
        """
        Initializes a new Transfer transaction.

        Inherits initialization from the `Transaction` model.
        """
        super().__init__(*args, **kwargs)

class PayBill(Transaction, Base):
    """
    Represents a bill payment transaction.

    This class defines the structure for storing and managing bill payments made by users. 
    It inherits common transaction attributes and functionality from the `Transaction` and `Base` classes.

    Attributes:
        __tablename__ (str): Name of the database table for bill payment transactions.
        account_no (Column): The account number from which the bill is paid.
        owner_customer_no (Column): The unique ID of the customer making the payment.
        transaction_type (Column): Specifies the type of transaction, defaulting to "paybill".
    """

    __tablename__ = "bill_payments"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    account_no = Column(String(100), nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    transaction_type = Column(String(20), nullable=False, default="paybill")


class BuyGoods(Transaction, Base):
    """
    Represents a transaction for buying goods and services.

    This class defines the structure for transactions related to the purchase of goods or services by a user. 
    It inherits common transaction attributes and functionality from the `Transaction` and `Base` classes.

    Attributes:
        __tablename__ (str): Name of the database table for buy goods transactions.
        owner_customer_no (Column): The unique ID of the customer making the purchase.
        transaction_type (Column): Specifies the type of transaction, defaulting to "buy_goods_and_services".
    """

    __tablename__ = "buy_goods_and_services"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    transaction_type = Column(String(23), nullable=False, default="buy_goods_and_services")


class Airtime(Transaction, Base):
    """
    Represents an airtime purchase transaction.

    This class handles transactions where users purchase airtime for mobile use. 
    It inherits common transaction attributes and functionality from the `Transaction` and `Base` classes.

    Attributes:
        __tablename__ (str): Name of the database table for airtime transactions.
        transaction_type (Column): Specifies the type of transaction, defaulting to "airtime".
        owner_customer_no (Column): The unique ID of the customer making the purchase.
    """

    __tablename__ = "airtime"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    transaction_type = Column(String(23), nullable=False, default="airtime")
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))


class TopUpWallet(Transaction, Base):
    """
    Represents a wallet top-up transaction.

    This class defines the structure for transactions where users transfer funds 
    from a bank account to their mobile wallets. It inherits common transaction 
    attributes and functionality from the `Transaction` and `Base` classes.

    Attributes:
        __tablename__ (str): Name of the database table for wallet top-up transactions.
        transaction_type (Column): Specifies the type of transaction, defaulting to "wallet_topup".
        owner_customer_no (Column): The unique ID of the customer initiating the wallet top-up.
        service_provider (Column): The name of the service provider receiving the top-up funds.
    """

    __tablename__ = "wallet_topups"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    transaction_type = Column(String(23), nullable=False, default="wallet_topup")
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    service_provider = Column(String(20), nullable=False)
