"""
Loan Application API Endpoints

This module provides an API endpoint for applying for personal loans. It handles loan creation, 
database transactions, and exception handling.

Modules and Dependencies:
- **FastAPI Components**: Includes router, Depends, status codes, and HTTP exception handling.
- **SQLAlchemy**: For ORM-based database transactions and session management.
- **Utilities**: Utility functions such as `save_prof` for additional operations.
- **Models and Schemas**: Defines ORM models and Pydantic schemas for loan applications and responses.

Classes:
    None

Functions:
    apply_personal_loan(new_loan: loans.PersonalLoanApplication, 
                        db: Session = Depends(get_db), 
                        current_user: str = Depends(oauth.get_current_user))
        Endpoint to create a personal loan application.

Modules Imported:
- `fastapi`: For API routing, request handling, and HTTP response management.
- `sqlalchemy`: For ORM database interactions.
- `uuid`: For generating unique account identifiers.
- `dateutil`: For advanced date and time calculations.
- `logging`: To log information and errors.

"""

from fastapi import Depends, status, APIRouter, HTTPException, File, Form, UploadFile
from .. import oauth
from typing import List
from dateutil.relativedelta import relativedelta
from datetime import datetime
from ..database import get_db
from sqlalchemy.orm import Session
from ..models.loans import PersonalLoans, BusinessLoans, Mortgages
from uuid import uuid4
from ..models.files import LoanDocs, MortgageDocs
import json
import logging
from ..schema import loans
from .utils.utils import save_prof

# Initialize the router for loan-related endpoints
# Set up router with a specific prefix for related endpoints
router = APIRouter(
    prefix="/post",
    tags=["Loan Services"],  # Assign this router to a specific documentation category
)
logger = logging.getLogger(__name__)

@router.post("/apply_personal_loan", 
             status_code=status.HTTP_201_CREATED, 
             response_model=loans.LoanSummary)
def apply_personal_loan(
    new_loan: loans.PersonalLoanApplication, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Apply for a personal loan.

    This endpoint allows authenticated users to apply for a personal loan by providing necessary loan details 
    via the payload. It saves the loan application to the database and returns the loan summary.

    Args:
        new_loan (loans.PersonalLoanApplication): Pydantic schema containing the payload for loan details such as amount and payback period.
        db (Session): Database session provided by FastAPI dependency injection.
        current_user (str): The authenticated user's identifier, provided by the OAuth dependency.

    Returns:
        loans.LoanSummary: A summary of the successfully created loan application, including the calculated maturity date 
        and outstanding amount.

    Raises:
        HTTPException: If an unexpected error occurs during loan creation or database transaction. Returns a 500 status 
        code with an error message.
    """
    try:
        loan = PersonalLoans(
            owner_customer_no=current_user.customer_no,
            account_no=str(uuid4()),
            maturity_date=datetime.now() + relativedelta(months=new_loan.payload['payback_period']),
            last_calculation_date=datetime.now(),
            disposable_amount=new_loan.payload['amount'],
            next_calculation_date=datetime.now() + relativedelta(days=1),
            outstanding_amount=new_loan.payload['amount'],
            id=str(uuid4()), 
            **new_loan.payload
        )
        # Add loan to the database session and commit
        db.add(loan)
        db.commit()
        db.refresh(loan)
        return loan

    except Exception as e:
        logger.error(f"Error during loan creation for user {current_user.customer_no}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.post(
    "/apply_business_loan",
    status_code=status.HTTP_201_CREATED,
    response_model=loans.LoanSummary,
    summary="Apply for a business loan",
    description="Allows authenticated users to apply for a business loan by uploading necessary documents "
                "and providing loan application details."
)
async def apply_business_loan(
    payload: str = Form(...),
    signature: str = Form(...),
    tax_cert: UploadFile = File(...),
    reg_cert: UploadFile = File(...),
    crb: UploadFile = File(...),
    operational_docs: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Handles business loan applications by processing uploaded documents and saving loan information.

    Args:
        payload (str): JSON string containing loan details.
        signature (str): A digital signature for loan application authorization.
        tax_cert (UploadFile): Upload file containing the tax certificate.
        reg_cert (UploadFile): Upload file containing the business registration certificate.
        crb (UploadFile): Upload file containing the CRB listing.
        operational_docs (UploadFile): Upload file containing operational documents.
        db (Session): The database session for transaction management.
        current_user (str): The authenticated user's identifier.

    Returns:
        loans.LoanSummary: Summary of the created loan application.

    Raises:
        HTTPException: If an error occurs during loan creation.
    """


@router.post(
    "/apply_mortgage",
    status_code=status.HTTP_201_CREATED,
    summary="Apply for a mortgage loan",
    description="Allows authenticated users to apply for a mortgage loan by uploading necessary documents "
                "and providing mortgage application details."
)
async def apply_mortgage(
    payload: str = Form(...),
    signature: str = Form(...),
    tax_cert: UploadFile = File(...),
    pay_slip: UploadFile = File(...),
    crb: UploadFile = File(...),
    down_payment: UploadFile = File(...),
    purchase_agreement: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Handles mortgage loan applications by processing uploaded documents and saving loan information.

    Args:
        payload (str): JSON string containing loan details.
        signature (str): A digital signature for loan application authorization.
        tax_cert (UploadFile): Upload file containing the tax certificate.
        pay_slip (UploadFile): Upload file containing the pay slip.
        crb (UploadFile): Upload file containing the CRB listing.
        down_payment (UploadFile): Upload file containing the proof of down payment.
        purchase_agreement (UploadFile): Upload file containing the purchase agreement.
        db (Session): The database session for transaction management.
        current_user (str): The authenticated user's identifier.

    Returns:
        Mortgages: Summary of the created mortgage application.

    Raises:
        HTTPException: If an error occurs during loan creation.
    """
    parsed_payload = loans.Mortgage(**json.loads(payload))
    mortgage = Mortgages(
        owner_customer_no=current_user.customer_no,
        maturity_date = datetime.now() + relativedelta(years=parsed_payload.payback_period),
        account_no=str(uuid4()),
        last_calculation_date=datetime.now(),
        next_calculation_date=datetime.now() + relativedelta(days=1),
        outstanding_amount=parsed_payload.amount,
        purpose="mortgage",
        **parsed_payload.dict()
    )
    
    tax_filename = save_prof(tax_cert)
    down_payment_filename = save_prof(down_payment)
    crb_filename = save_prof(crb)
    purchase_agreement_filename = save_prof(purchase_agreement)
    pay_slip_filename = save_prof(pay_slip)

    files = [tax_cert, pay_slip, crb, purchase_agreement, down_payment]
    for file in files:
        filename = save_prof(file)
        file_location = f"uploads/loan_documents/{filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
    taxcertificate = MortgageDocs(name=tax_filename, doc_type="tax-certificate", mortgage_document=mortgage)
    down_payment_cert = MortgageDocs(name=down_payment_filename, doc_type="down_payment", mortgage_document=mortgage)
    crb_listing = MortgageDocs(name=crb_filename, doc_type="crb-listing", mortgage_document=mortgage)
    purchase_agreement_cert = MortgageDocs(name=purchase_agreement_filename, doc_type="purchase_agreement", mortgage_document=mortgage)
    pay_slip_cert = MortgageDocs(name=pay_slip_filename, doc_type="pay-slip", mortgage_document=mortgage)

    try:
        db.add_all([taxcertificate, down_payment_cert, purchase_agreement_cert, mortgage, crb_listing, pay_slip_cert])
        db.commit()
        db.refresh(mortgage)
        logger.info(f"Account created successfully for user {current_user.customer_no}.")
        return mortgage
    except Exception as e:
        logger.error(f"Error creating account for user {current_user.customer_no}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the account."
        )

@router.get(
    "/get_user_loans",
    status_code=status.HTTP_200_OK, 
    response_model=List[loans.LoanSummary1]
)
def get_user_loans(
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Retrieve current and savings accounts for the user.

    This endpoint fetches all "Pay As You Go" and "Savings Account" type accounts associated 
    with the currently authenticated user.

    Args:
        db (Session): The database session used for queries.
        current_user (str): The currently authenticated user.

    Returns:
        List[loans.LoanSummary]: A list of current and savings accounts owned by the user.
    """
    personal_loans = db.query(PersonalLoans).filter(
        PersonalLoans.owner_customer_no == current_user.customer_no,
    ).all()
    business_loans = db.query(BusinessLoans).filter(
        BusinessLoans.owner_customer_no == current_user.customer_no
    ).all()

    accounts = personal_loans + business_loans
    for account in accounts:
        account.truncate_uuid()
        account.format_cash()
    return accounts



@router.get(
    "/get_user_transactive_loans",
    status_code=status.HTTP_200_OK,
    response_model=List[loans.ResponseLoan]
)
def get_user_transactive_loans(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    personal_loan_accounts = db.query(PersonalLoans).filter(
        PersonalLoans.owner_customer_no == current_user.customer_no,
        PersonalLoans.account_status == "in-review"
    ).all()
    business_loan_accounts = db.query(BusinessLoans).filter(
        BusinessLoans.owner_customer_no == current_user.customer_no,
        BusinessLoans.account_status == "in-review"
    ).all()
    accounts = personal_loan_accounts + business_loan_accounts
    for account in accounts:
        account.account_balance = account.disposable_amount
    return accounts