from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from .. import oauth
from typing import List
from dateutil.relativedelta import relativedelta
from ..models.term_deposits import TermDeposit
from datetime import datetime
from ..schema import term_deposits
from ..database import get_db
from sqlalchemy.orm import Session
from ..models.accounts import PersonalAccounts, CorporateAccounts
from uuid import uuid4

# Define the available account CLASSES for querying
CLASSES = [PersonalAccounts, CorporateAccounts]

# Initialize the router for the "/post" prefix
router = APIRouter(prefix="/post")

# POST endpoint to book a term deposit
@router.post("/book_td", status_code=status.HTTP_201_CREATED, response_model=term_deposits.TDSummary)
def book_td(
    new_request: term_deposits.BookTD,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Books a new term deposit for the user.

    - Verifies that the provided account exists and has sufficient funds.
    - Creates a new TermDeposit entry in the database.
    - Deducts the deposit amount from the account balance.

    Args:
        new_request (term_deposits.BookTD): Request body containing the details for booking the term deposit.
        db (Session): Database session.
        current_user (str): Currently authenticated user.

    Returns:
        term_deposits.TDSummary: The created term deposit summary.
    """
    # Attempt to find the account associated with the deposit
    account = None
    for clss in CLASSES:
        account = db.query(clss).filter(clss.account_no == new_request.payload['account']).first()
        if account:
            break

    try:
        # Validate account existence and other conditions
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account does not exist."
            )
        if new_request.payload['amount'] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction amount must be greater than zero."
            )
        if account.account_balance < new_request.payload['amount']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient funds in the account."
            )

        # Create the TermDeposit object and update the account balance
        maturity_date = datetime.now() + relativedelta(months=new_request.payload['maturity_period'])
        term_deposit = TermDeposit(
            owner_customer_no=current_user.customer_no,
            account_no=uuid4(),  # Generate a unique account number for the term deposit
            maturity_date=maturity_date,
            accumulated_value=new_request.payload['amount'],
            id=uuid4(),  # Generate a unique ID for the term deposit
            **new_request.payload
        )
        account.account_balance -= new_request.payload['amount']  # Deduct the amount from the account balance

        # Save the term deposit and commit the transaction
        db.add(term_deposit)
        db.commit()
        db.refresh(term_deposit)

        return term_deposit

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while processing your request."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

# GET endpoint to fetch the user's active term deposits
@router.get("/get_user_term_deposits", status_code=status.HTTP_200_OK, response_model=List[term_deposits.ChildTDSummary])
def get_user_tds(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Retrieves a list of active term deposits for the currently authenticated user.

    Args:
        db (Session): Database session.
        current_user (str): Currently authenticated user.

    Returns:
        List[term_deposits.ChildTDSummary]: List of active term deposit summaries.
    """
    # Query active term deposits for the user
    term_deposits = db.query(TermDeposit).filter(
        TermDeposit.owner_customer_no == current_user.customer_no,
        TermDeposit.status == "active"
    ).all()

    # Process each term deposit (formatting, truncating, and calculating days remaining)
    for td in term_deposits:
        td.format_cash()
        td.truncate_datetime()
        td.days_remaining()

    return term_deposits

# POST endpoint to liquidate a term deposit
@router.post("/liquidate", status_code=status.HTTP_201_CREATED)
def liquidate_td(
    term_deposit: term_deposits.Liquidate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Liquidates an active term deposit, returning the principal amount to the associated account.

    - Verifies that the term deposit exists and is active.
    - Updates the associated account balance.
    - Changes the term deposit status to "liquidated".

    Args:
        term_deposit (term_deposits.Liquidate): Request body containing the term deposit account number to be liquidated.
        db (Session): Database session.
        current_user (str): Currently authenticated user.

    Returns:
        HTTPStatus: 201 if liquidation is successful.
    """
    try:
        # Find the term deposit to liquidate
        td = db.query(TermDeposit).filter(TermDeposit.account_no == term_deposit.payload['account_no']).first()
        if not td:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Term deposit not found."
            )

        # Find the associated account
        account = None
        for clss in CLASSES:
            account = db.query(clss).filter(clss.account_no == td.account).first()
            if account:
                break

        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Associated account not found."
            )

        # Return the deposit amount to the account and update the term deposit status
        account.account_balance += td.amount
        td.status = "liquidated"
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
