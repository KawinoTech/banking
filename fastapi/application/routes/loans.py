from fastapi import  Depends, status, APIRouter, HTTPException, status, File, Form, UploadFile
from sqlalchemy.exc import IntegrityError
from .. import schemas, oauth
from typing import List
from dateutil.relativedelta import relativedelta
from datetime import datetime
from ..database import  get_db
from sqlalchemy.orm import Session
from ..models.loans import PersonalLoans, BusinessLoans, Mortgages
from uuid import uuid4
from ..models.files import LoanDocs, MortgageDocs
import json
import logging
from .utils.utils import save_prof

router = APIRouter(prefix="/post")
logger = logging.getLogger(__name__)


@router.post("/apply_personal_loan", status_code=status.HTTP_201_CREATED, response_model=schemas.LoanSummary)
def apply_personal_loan(new_loan: schemas.PersonalLoanApplication, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):

    try:
        loan = PersonalLoans(owner_customer_no = current_user.customer_no,
                            account_no=uuid4(),
                            maturity_date=datetime.now() + relativedelta(months=new_loan.payload['payback_period']),
                            last_calculation_date=datetime.now(),
                            disposable_amount=new_loan.payload['amount'],
                            next_calculation_date=datetime.now() + relativedelta(days=1),
                            outstanding_amount=new_loan.payload['amount'],
                            id = uuid4(), **new_loan.payload)
        db.add(loan)
        db.commit()
        db.refresh(loan)
        return loan

    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.post(
    "/apply_business_loan",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.LoanSummary,
    summary="Create a new personal account",
    description="Allows authenticated users to create a new personal account. Each account is uniquely identified, "
                "associated with the current user, and validated to ensure compliance with account type restrictions."
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
    parsed_payload = schemas.BusinessLoanApplication(**json.loads(payload))
    loan = BusinessLoans(
        owner_customer_no=current_user.customer_no,
        maturity_date = datetime.now() + relativedelta(months=parsed_payload.payback_period),
        last_calculation_date=datetime.now(),
        next_calculation_date=datetime.now() + relativedelta(days=1),
        outstanding_amount=parsed_payload.amount,
        disposable_amount=parsed_payload.amount,
        account_no=str(uuid4()),
        **parsed_payload.dict()
    )
    
    tax_filename = save_prof(tax_cert)
    reg_filename = save_prof(reg_cert)
    crb_filename = save_prof(crb)
    operational_docs_filename = save_prof(operational_docs)

    files = [tax_cert, reg_cert, crb, operational_docs]
    for file in files:
        filename = save_prof(file)
        file_location = f"uploads/loan_documents/{filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
    taxcertificate = LoanDocs(name=tax_filename, doc_type="tax-certificate", business_loan_document=loan)
    bus_registration = LoanDocs(name=reg_filename, doc_type="business-registration", business_loan_document=loan)
    crb_listing = LoanDocs(name=crb_filename, doc_type="crb-listing", business_loan_document=loan)
    operational_docs = LoanDocs(name=operational_docs_filename, doc_type="operational-docs", business_loan_document=loan)

    try:
        db.add_all([taxcertificate, bus_registration, operational_docs, loan, crb_listing])
        db.commit()
        db.refresh(loan)
        logger.info(f"Account created successfully for user {current_user.customer_no}.")
        return loan
    except Exception as e:
        logger.error(f"Error creating account for user {current_user.customer_no}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the account."
        )


@router.post(
    "/apply_mortgage",
    status_code=status.HTTP_201_CREATED,
    #response_model=schemas.LoanSummary,
    summary="Create a new personal account",
    description="Allows authenticated users to create a new personal account. Each account is uniquely identified, "
                "associated with the current user, and validated to ensure compliance with account type restrictions."
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
    parsed_payload = schemas.Mortgage(**json.loads(payload))
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
    response_model=List[schemas.LoanSummary]
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
        List[schemas.ResponseAccount1]: A list of current and savings accounts owned by the user.
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
    return accounts