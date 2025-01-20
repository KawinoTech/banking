from fastapi import Depends, status, APIRouter, HTTPException
import logging
from datetime import datetime
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
from ..models.transactions import PayBill, BuyGoods, Transfer, Airtime
from ..models.users import Customer
from ..models.accounts import PersonalAccounts, CorporateAccounts

from .. import schemas, oauth
from ..database import get_db

DAILY_LIMIT = 100
classes = [PersonalAccounts, CorporateAccounts]
router = APIRouter(prefix="/post")
logger = logging.getLogger(__name__)

@router.post(
    "/transfer",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseTransact,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    tags=["transactions"],
    summary="Transfer funds between accounts",
    description="Allows users to transfer funds from bank accounts to mobile accounts (MPESA, AIRTEL, Telcom) adhering to specified limits."
)
def transfer(
    transaction: schemas.Transaction,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Transfer funds between accounts.

    Args:
        transaction (schemas.Transaction): The transaction payload containing account details and the amount.
        db (Session): Database session.
        current_user (str): The authenticated user.

    Returns:
        schemas.ResponseTransact: Details of the transaction.

    Raises:
        HTTPException: Various HTTP exceptions based on transaction validity and errors.
    """
    new_transaction = Transfer(
        id=uuid4(),
        ref_no=uuid4(),
        date_posted=datetime.now(),
        **transaction.payload,
        owner_customer_no=current_user.customer_no
    )
    for clss in classes:
        account = db.query(clss).filter(
            clss.account_no == transaction.payload['account']
        ).first()
        if account:
            break

    try:
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account does not exist."
            )
        if transaction.payload['amount'] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction amount must be greater than zero."
            )
        if account.account_balance < transaction.payload['amount']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed. Insufficient funds."
            )

        account.account_balance -= transaction.payload['amount']
        new_transaction.generate_ref_number()
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        logger.info(
            f"User {current_user} transferred {transaction.payload['amount']} "
            f"from account {transaction.payload['account']}"
        )
        return new_transaction

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
    finally:
        db.close()


@router.post(
    "/buygoods",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseTransact,
    tags=["transactions"],
    summary="Buy goods and services",
    description="Allows users to purchase goods and services using funds from their account, ensuring that all transactions adhere to account balance limits.",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
def buygoods(
    transaction: schemas.Transaction,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Handle transactions for purchasing goods and services.

    This endpoint allows a user to initiate a transaction for buying goods or services. 
    It validates the user's account existence, ensures sufficient funds, and deducts the 
    appropriate amount from the account balance. A new transaction record is created and stored.

    Args:
        transaction (schemas.Transaction): The payload containing the account details and transaction amount.
        db (Session): The database session used to interact with the database.
        current_user (str): The currently authenticated user performing the transaction.

    Returns:
        schemas.ResponseTransact: The details of the successful transaction, including IDs and reference numbers.

    Raises:
        HTTPException: 
            - 404 Not Found: If the specified account does not exist.
            - 400 Bad Request: If the transaction amount is invalid (<= 0).
            - 501 Not Implemented: If the account has insufficient funds.
            - 500 Internal Server Error: If a database error or unexpected error occurs.
    """
    new_transaction = BuyGoods(
        id=uuid4(),
        ref_no=uuid4(),
        date_posted=datetime.now(),
        **transaction.payload,
        owner_customer_no=current_user.customer_no
    )
    for clss in classes:
        account = db.query(clss).filter(
            clss.account_no == transaction.payload['account']
        ).first()
        if account:
            break

    try:
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account does not exist."
            )
        if transaction.payload['amount'] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction amount must be greater than zero."
            )
        if account.account_balance < transaction.payload['amount']:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Failed. Insufficient funds."
            )

        account.account_balance -= transaction.payload['amount']
        new_transaction.generate_ref_number()
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        logger.info(
            f"User {current_user} completed a purchase of {transaction.payload['amount']} "
            f"from account {transaction.payload['account']}."
        )
        return new_transaction


    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )



@router.post(
    "/paybill",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseTransact,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    tags=["transactions"],
    summary="Pay utility bills",
    description="Allows users to make payments for utility bills (e.g., electricity, water, or other services) "
                "using funds from their bank accounts while ensuring account balance sufficiency."
)
def paybill(
    transaction: schemas.Transaction,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Handle payments for utility bills.

    This endpoint facilitates the payment of bills such as utilities or other services 
    from a user’s account. It checks for account existence, validates the transaction amount,
    ensures there are sufficient funds, and creates a new transaction record upon success.

    Args:
        transaction (schemas.Transaction): The payload containing the account details and bill payment amount.
        db (Session): The database session used for database operations.
        current_user (str): The currently authenticated user performing the transaction.

    Returns:
        schemas.ResponseTransact: The details of the successfully processed transaction.

    Raises:
        HTTPException:
            - 404 Not Found: If the specified account does not exist.
            - 400 Bad Request: If the transaction amount is invalid (<= 0).
            - 501 Not Implemented: If the account has insufficient funds.
            - 500 Internal Server Error: If a database error or unexpected error occurs.
    """
    new_transaction = PayBill(
        id=uuid4(),
        ref_no=uuid4(),
        **transaction.payload,
        date_posted=datetime.now(),
        owner_customer_no=current_user.customer_no
    )
    for clss in classes:
        account = db.query(clss).filter(
            clss.account_no == transaction.payload['account']
        ).first()
        if account:
            break

    try:
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account does not exist."
            )
        if transaction.payload['amount'] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction amount must be greater than zero."
            )
        if account.account_balance < transaction.payload["amount"]:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Failed. Insufficient funds."
            )

        account.account_balance -= transaction.payload["amount"]
        new_transaction.generate_ref_number()
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        logger.info(
            f"User {current_user} made a bill payment of {transaction.payload['amount']} "
            f"from account {transaction.payload['account']}."
        )
        return new_transaction

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get(
    "/all_user_transactions",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.AllTransactions],
    summary="Retrieve all user transactions",
    description="Fetches all transactions performed by the current user, categorized by type, "
                "including customer-to-business transactions, bill payments, and goods/services purchases."
)
def all_user_transactions(
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Retrieve all transactions for the current user.

    This endpoint allows the authenticated user to view a summary of all their transactions, 
    grouped by type. It fetches customer-to-business (C2B) transactions, bill payments, and 
    purchases of goods and services, formats the data for clarity, and returns a consolidated list.

    Args:
        db (Session): The database session for querying the database.
        current_user (str): The currently authenticated user.

    Returns:
        List[schemas.AllTransactions]: A list of all transactions associated with the user, 
        grouped by type and properly formatted.

    Raises:
        HTTPException:
            - 404 Not Found: If the user is not found in the database.
            - 500 Internal Server Error: If an error occurs during data retrieval or processing.

    Note:
        - The function calls methods on the `user` model to fetch categorized transactions.
        - Each transaction undergoes formatting steps for UUID truncation and cash formatting.
    """
    user = db.query(Customer).filter(Customer.customer_no == current_user.customer_no).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    try:
        # Fetch categorized transactionss
        c2b_transactions = user.get_c2b_transactions(db)
        bills = user.get_bills(db)
        goods_and_services = user.get_amount(db)
        airtime = user.get_airtime(db)

        # Consolidate all transactions
        all_transactions = c2b_transactions + bills + goods_and_services + airtime

        # Format transaction details
        for transaction in all_transactions:
            transaction.truncate_uuid()
            transaction.format_cash()
            transaction.truncate_datetime()

        return all_transactions

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching transactions: {str(e)}"
        )

@router.post(
    "/airtime",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseTransact,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    tags=["transactions"],
    summary="Transfer funds between accounts",
    description="Allows users to transfer funds from bank accounts to mobile accounts (MPESA, AIRTEL, Telcom) adhering to specified limits."
)
def buy_airtime(
    transaction: schemas.Transaction,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Transfer funds between accounts.

    Args:
        transaction (schemas.Transaction): The transaction payload containing account details and the amount.
        db (Session): Database session.
        current_user (str): The authenticated user.

    Returns:
        schemas.ResponseTransact: Details of the transaction.

    Raises:
        HTTPException: Various HTTP exceptions based on transaction validity and errors.
    """
    new_transaction = Airtime(
        id=uuid4(),
        remarks="airtime",
        ref_no=uuid4(),
        date_posted=datetime.now(),
        **transaction.payload,
        owner_customer_no=current_user.customer_no
    )
    for clss in classes:
        account = db.query(clss).filter(
            clss.account_no == transaction.payload['account']
        ).first()
        if account:
            break

    try:
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account does not exist."
            )
        if transaction.payload['amount'] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction amount must be greater than zero."
            )
        if account.account_balance < transaction.payload['amount']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed. Insufficient funds."
            )

        account.account_balance -= transaction.payload['amount']
        new_transaction.generate_ref_number()
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        logger.info(
            f"User {current_user} transferred {transaction.payload['amount']} "
            f"from account {transaction.payload['account']}"
        )
        return new_transaction


    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    finally:
        db.close()