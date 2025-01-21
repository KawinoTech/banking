from fastapi import  Depends, status, APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from .. import schemas, oauth
from typing import List
from dateutil.relativedelta import relativedelta
from ..models.term_deposits import TermDeposit
from datetime import datetime
from ..database import  get_db
from sqlalchemy.orm import Session
from ..models.accounts import PersonalAccounts, CorporateAccounts
from uuid import uuid4
classes = [PersonalAccounts, CorporateAccounts]
router = APIRouter(prefix="/post")

classes = [PersonalAccounts, CorporateAccounts]

@router.post("/book_td", status_code=status.HTTP_201_CREATED, response_model=schemas.TDSummary)
def book_td(new_request: schemas.BookTD, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    for clss in classes:
        account = db.query(clss).filter(
            clss.account_no == new_request.payload['account']
        ).first()
        if account:
            break

    try:
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
                detail="Failed. Insufficient funds."
            )
        request = TermDeposit(owner_customer_no = current_user.customer_no,
                            account_no=uuid4(),
                            maturity_date=datetime.now() + relativedelta(months=new_request.payload['maturity_period']),
                            id = uuid4(), **new_request.payload)
        account.account_balance -= new_request.payload['amount']
        db.add(request)
        db.commit()
        db.refresh(request)
        return request
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get(
    "/get_user_term_deposits", 
    status_code=status.HTTP_200_OK, 
    response_model=List[schemas.ChildTDSummary]
)
def get_user_tds(
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Retrieve all user accounts.

    This endpoint fetches all accounts associated with the currently authenticated user.

    Args:
        db (Session): The database session used for queries.
        current_user (str): The currently authenticated user.

    Returns:
        List[schemas.ResponseAccount1]: A list of accounts owned by the user.
    """
    term_deposits = db.query(TermDeposit).filter(
        TermDeposit.owner_customer_no == current_user.customer_no,
        TermDeposit.status == "active"
    ).all()
    for td in term_deposits:
        td.format_cash()
        td.truncate_datetime()
        td.days_remaining()
    return term_deposits

@router.post("/liquidate", status_code=status.HTTP_201_CREATED)
def liquidate_td(term_deposit: schemas.Liquidate, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    try:
        print(term_deposit.payload['account_no'])
        td = db.query(TermDeposit).filter(TermDeposit.account_no == term_deposit.payload['account_no']).first()
        if not td:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deposit not found."
            )
        for clss in classes:
            account = db.query(clss).filter(
                clss.account_no == td.account
            ).first()
            if account:
                break
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account does not exist."
            )
        account.account_balance += td.amount
        td.status = "liquidated"
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )