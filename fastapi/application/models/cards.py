"""
Card Models Module.

This module defines various models representing different types of cards, such as prepaid, credit, and debit cards.
All card models inherit common fields and methods from the `BaseCards` class, which itself extends the `BaseModel` class.
The models are designed for integration with a database using SQLAlchemy, facilitating ORM functionality.

Models:
    - BaseCards: The base model for all card types, containing common fields and utility methods.
    - PrepaidCards: Represents a prepaid card with specific attributes and functionality.
    - CreditCards: Represents a credit card, including attributes such as balance, interest rate, and credit limit.
    - DebitCards: Represents a debit card, including attributes like the attached account number and classification.

Usage:
    These models can be used in a SQLAlchemy-based application to interact with database records.
    They provide pre-defined fields and methods for operations such as generating card numbers, formatting them, and truncating sensitive information.
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Float, Text, DateTime
from .base_model import BaseModel
from . import Base
import random
import string

class BaseCards(BaseModel):
    """
    Represents the base card model that other card models inherit from.

    Attributes:
        full_name (str): Full name of the card owner.
        email_address (str): Email address of the card owner.
        phone (str): Phone number of the card owner.
        date_issued (datetime): The issuance date of the card.
        status (str): The status of the card (e.g., 'Active', 'Inactive'). Defaults to 'Inactive'.
        expiry_date (datetime): The expiration date of the card.
        currency (str): The currency of the card. Defaults to 'KES'.
        delivery_option (str): Delivery option chosen for the card.
        loyalty_point (float): Loyalty points associated with the card. Defaults to 1.0.
        card_no (str): The unique card number, which serves as the primary key.
    """
    full_name = Column(String(70), nullable=False)
    email_address = Column(String(30), nullable=False)
    phone = Column(String(15), nullable=False)
    date_issued = Column(DateTime, nullable=False)
    status = Column(String(10), nullable=False, default="Inactive")
    expiry_date = Column(DateTime, nullable=False)
    currency = Column(String(4), nullable=False, default='KES')
    delivery_option = Column(String(20), nullable=False)
    loyalty_point = Column(Float, nullable=False, default=1.0)
    card_no = Column(String(17), primary_key=True)

    @staticmethod
    def generate_card_no():
        """
        Generate a random 16-digit card number.

        Returns:
            str: A randomly generated card number.
        """
        return ''.join(random.choices(string.digits, k=16))

    def reformat_card_no(self):
        """
        Format the card number into groups of four digits separated by hyphens.
        """
        self.card_no = '-'.join(self.card_no[i:i+4] for i in range(0, 16, 4))

    def truncate_uuid(self):
        """
        Truncate the account UUID for display purposes, maintaining clarity and security.
        """
        uuid = self.account_attached_no
        parts = uuid.split('-')
        truncated = f"{parts[0]}-***-{parts[-1][-2:]}"
        self.account_attached_no = truncated

    def truncate_datetime(self, format: str = "%Y-%m-%d %H:%M:%S"):
        """
        Truncate datetime fields for readability.

        Args:
            format (str): The datetime format to use. Defaults to "%Y-%m-%d %H:%M:%S".
        """
        self.date_issued = self.date_issued.strftime(format).split(' ')[0]
        self.expiry_date = self.expiry_date.strftime(format).split(' ')[0]

class PrepaidCards(BaseCards, Base):
    """
    Represents a prepaid card.

    Attributes:
        card_type (str): The type of card, default is 'prepaid'.
        balance (int): Initial balance on the card. Defaults to 50,000.
        intended_usage (str): The intended usage for the prepaid card.
        owner_customer_no (int): The owner customer number linking to the customers table.
    """
    __tablename__ = "prepaid_cards"
    card_type = Column(String(8), nullable=False, default="prepaid")
    balance = Column(Integer, nullable=False, default=50000)
    intended_usage = Column(Text, nullable=False)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'), nullable=False)

class CreditCards(BaseCards, Base):
    """
    Represents a credit card.

    Attributes:
        card_type (str): The type of card, default is 'credit'.
        balance (int): Current balance of the credit card. Defaults to 0.
        due_date (datetime): Due date for payments.
        annual_income (int): Annual income of the card owner.
        employment_status (str): Employment status of the card owner.
        rate (float): Interest rate on the credit card. Defaults to 3.2.
        owner_customer_no (int): The owner customer number linking to the customers table.
        limit (str): Credit limit assigned to the card. Defaults to "Not Assigned".
        card_classification (str): Classification of the card (e.g., 'Gold', 'Platinum').
    """
    __tablename__ = "credit_cards"
    card_type = Column(String(7), nullable=False, default="credit")
    balance = Column(Integer, nullable=False, default=0)
    due_date = Column(DateTime, nullable=False)
    annual_income = Column(Integer, nullable=True)
    employment_status = Column(String(20), nullable=True)
    rate = Column(Float, nullable=False, default=3.2)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    limit = Column(String(20), nullable=False, default="Not Assigned")
    card_classification = Column(String(20), nullable=False)

class DebitCards(BaseCards, Base):
    """
    Represents a debit card.

    Attributes:
        card_type (str): The type of card, default is 'debit'.
        account_attached_no (str): The account number attached to the debit card.
        owner_customer_no (int): The owner customer number linking to the customers table.
        card_classification (str): Classification of the card (e.g., 'Standard', 'Premium').
    """
    __tablename__ = "debit_cards"
    card_no = Column(String(17), primary_key=True)
    card_type = Column(String(5), nullable=False, default="debit")
    account_attached_no = Column(String(50), ForeignKey('personal_accounts.account_no'), nullable=True)
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    card_classification = Column(String(20), nullable=False)
