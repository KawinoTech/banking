"""
Schema Definitions Documentation

This module contains Pydantic models used for data validation and serialization across different endpoints of the loan application system. These models define the structure for incoming requests and outgoing responses related to personal loans, business loans, mortgages, and loan summaries.

Modules and Dependencies:
- `Pydantic` for model validation and serialization.

Classes:
    - `PersonalLoanApplication`: Represents the structure for personal loan application payloads.
    - `BusinessLoanApplication`: Represents the structure for business loan application data.
    - `Mortgage`: Defines the schema for mortgage applications.
    - `LoanSummary` & `LoanSummary1`: Models for summarizing loan details.
    - `ResponseLoan`: Represents the structure of a general loan response.

Attributes:
    Each class contains attributes tailored to its specific use case, ensuring precise validation and compatibility with API requirements.
"""

from pydantic import BaseModel


class PersonalLoanApplication(BaseModel):
    """
    Represents the structure for personal loan application payloads.

    Attributes:
        payload (dict): Contains application details including the loan parameters.
        signature (str): Digital signature of the applicant for verification.
    """
    payload: dict
    signature: str


class LoanSummary(BaseModel):
    """
    Represents a summarized view of loan details.

    Attributes:
        amount (int): Total amount of the loan.
        account_no (str): Unique identifier for the loan account.
        payback_period (int): Duration of the loan repayment period in months.
        purpose (str): The purpose for which the loan is taken.
        outstanding_amount (float): Remaining balance to be repaid.
        account_type (str): Type of loan account.
        accrued_interest (float): Total accrued interest on the loan.
        principal_paid (float): Amount of principal already paid.
    """
    amount: int
    account_no: str
    payback_period: int
    purpose: str
    outstanding_amount: float
    account_type: str
    accrued_interest: float
    principal_paid: float


class LoanSummary1(BaseModel):
    """
    A variation of the `LoanSummary` schema allowing string values for numeric fields.

    Attributes:
        amount (str): Total amount of the loan (as a string).
        account_no (str): Unique identifier for the loan account.
        payback_period (int): Duration of the loan repayment period in months.
        purpose (str): The purpose for which the loan is taken.
        outstanding_amount (str): Remaining balance to be repaid (as a string).
        disposable_amount (str): Disposable income or funds available for loan payment.
        account_type (str): Type of loan account.
        accrued_interest (float): Total accrued interest on the loan.
        principal_paid (float): Amount of principal already paid.
    """
    amount: str
    account_no: str
    payback_period: int
    purpose: str
    outstanding_amount: str
    disposable_amount: str
    account_type: str
    accrued_interest: float
    principal_paid: float


class BusinessLoanApplication(BaseModel):
    """
    Represents the structure for business loan application data.

    Attributes:
        id_no (str): Identification number of the business owner.
        purpose (str): The purpose for which the loan is required.
        payback_period (int): Loan repayment duration in months.
        account_name (str): Name of the account associated with the loan.
        address (str): Address of the business or applicant.
        pmargin (float): Profit margin for the business.
        dob (str): Date of birth of the applicant.
        annual_income (float): Annual income of the business or applicant.
        amount (float): Amount requested for the loan.
    """
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
    """
    Represents the schema for mortgage applications.

    Attributes:
        account_name (str): Name associated with the mortgage account.
        employment_status (str): Employment status of the applicant.
        annual_income (float): Applicant's annual income.
        payback_period (int): Payback period for the mortgage in years.
        property_address (str): Address of the property for the mortgage.
        property_value (float): Valuation of the mortgaged property.
        down_payment (float): Amount paid upfront for the property.
        amount (float): Total loan amount requested.
        property_type (str): Type of property being mortgaged (e.g., residential, commercial).
        rate (int): Interest rate for the mortgage.
    """
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


class ResponseLoan(BaseModel):
    """
    Represents the structure of a generic loan response.

    Attributes:
        account_no (str): Unique identifier for the loan account.
        account_balance (int): Current balance of the loan account.
        account_type (str): Type of loan account.
        currency (str): Currency used for the loan.
    """
    account_no: str
    account_balance: int
    account_type: str
    currency: str
