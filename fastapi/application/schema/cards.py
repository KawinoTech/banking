from datetime import datetime
from pydantic import BaseModel

class CardApplicationResponse(BaseModel):
    """
    Represents the response structure for a card application.

    Attributes:
        full_name (str): The full name of the cardholder.
        email_address (str): Email address associated with the cardholder.
        phone (str): Contact phone number for the cardholder.
        card_type (str): Type of card applied for (e.g., Debit, Credit, Prepaid).
        delivery_option (str): Method of delivery for the card.
        card_no (str): Generated unique card number.
        status (str): Status of the application (e.g., Pending, Approved, Rejected).
        date_issued (datetime): The date the card was issued.
        expiry_date (datetime): Expiration date of the card.
    """
    full_name: str
    email_address: str
    phone: str
    card_type: str
    delivery_option: str
    card_no: str
    status: str
    date_issued: datetime
    expiry_date: datetime

class GetDebitCards(BaseModel):
    """
    Represents the details of debit cards associated with a user.

    Attributes:
        full_name (str): Full name of the cardholder.
        card_type (str): Type of card.
        card_classification (str): Classification or tier of the card.
        card_no (str): Partially obfuscated card number.
        account_attached_no (str): Associated account number.
        status (str): Current status of the card (e.g., Active, Blocked).
        date_issued (str): Formatted issue date.
        expiry_date (str): Formatted expiration date.
    """
    full_name: str
    card_type: str
    card_classification: str
    card_no: str
    account_attached_no: str
    status: str
    date_issued: str
    expiry_date: str

class GetCreditCards(BaseModel):
    """
    Represents the details of credit cards associated with a user.

    Attributes:
        full_name (str): Full name of the cardholder.
        balance (int): Current balance on the card.
        due_date (datetime): Payment due date for the card.
        card_classification (str): Classification or tier of the card.
        card_no (str): Partially obfuscated card number.
        status (str): Current status of the card (e.g., Active, Blocked).
        date_issued (str): Formatted issue date.
        expiry_date (str): Formatted expiration date.
        limit (str): Credit limit of the card.
    """
    full_name: str
    balance: int
    due_date: datetime
    card_classification: str
    card_no: str
    status: str
    date_issued: str
    expiry_date: str
    limit: str

class GetPrepaidCards(BaseModel):
    """
    Represents the details of prepaid cards associated with a user.

    Attributes:
        full_name (str): Full name of the cardholder.
        balance (int): Current available balance on the card.
        card_no (str): Partially obfuscated card number.
        status (str): Current status of the card (e.g., Active, Blocked).
        date_issued (str): Formatted issue date.
        expiry_date (str): Formatted expiration date.
    """
    full_name: str
    balance: int
    card_no: str
    status: str
    date_issued: str
    expiry_date: str

class CardApplication(BaseModel):
    """
    Represents the structure for submitting a card application request.

    Attributes:
        payload (dict): A dictionary containing the application data (e.g., card type, user details).
        signature (str): A digital signature validating the request.
    """
    payload: dict
    signature: str
