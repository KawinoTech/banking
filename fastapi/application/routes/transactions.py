from fastapi import Depends, status, APIRouter, HTTPException
import logging
from datetime import datetime
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
from ..models.transactions import Transfer, BuyGoods, PayBill, Airtime, TopUpWallet
from ..models.accounts import PersonalAccounts, CorporateAccounts
from ..models.loans import PersonalLoans, BusinessLoans
from ..models.users import Customer
from .. import oauth
from ..schema import transactions
from ..database import get_db

# Constants
DAILY_LIMIT = 100
ACCOUNT_CLASSES = [PersonalAccounts, CorporateAccounts, BusinessLoans, PersonalLoans]

# Router initialization
# Set up router with a specific prefix for related endpoints
router = APIRouter(
    prefix="/post",
    tags=["Customer Transaction"],  # Assign this router to a specific documentation category
)

logger = logging.getLogger(__name__)

@router.post(
    "/transfer",
    status_code=status.HTTP_201_CREATED,
    response_model=transactions.ResponseTransact,
    dependencies=[Depends(RateLimiter(times=1, seconds=60))],
    tags=["transactions"],
    summary="Transfer funds between accounts",
    description="Allows users to transfer funds between accounts, including mobile payments (MPESA, Airtel, Telcom), respecting transaction limits."
)
def transfer(
    transaction: transactions.Transaction,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Process a fund transfer between accounts.
    
    Args:
        transaction (schemas.Transaction): The transaction details including account, amount, etc.
        db (Session): The database session.
        current_user (str): The authenticated user's information.
        
    Returns:
        schemas.ResponseTransact: The transaction result.
    
    Raises:
        HTTPException: Includes error details for issues like account not found or insufficient funds.
    """
    
    # Initialize transaction object
    new_transaction = Transfer(
        id=uuid4(),
        ref_no=uuid4(),
        date_posted=datetime.now(),
        **transaction.payload,
        owner_customer_no=current_user.customer_no
    )
    
    # Search for the account associated with the transaction
    account = None
    for account_class in ACCOUNT_CLASSES:
        account = db.query(account_class).filter(account_class.account_no == transaction.payload['account']).first()
        if account:
            break

    try:
        # Validation checks
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
        if account.account_type == "Personal Loan" or account.account_type == "Business Loan":
            if account.disposable_amount < transaction.payload['amount']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds for this transaction."
                )
            else:
                account.disposable_amount -= transaction.payload['amount']
        else:
            if account.account_balance < transaction.payload['amount']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds for this transaction."
                )
            else:
                 account.account_balance -= transaction.payload['amount']

        # Process the transaction
        new_transaction.generate_ref_number()  # Ensure that the reference number is generated

        # Save the transaction and commit
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        # Log the transaction success
        logger.info(
            f"User {current_user} successfully transferred {transaction.payload['amount']} "
            f"from account {transaction.payload['account']}."
        )

        return new_transaction

    except IntegrityError as e:
        # Handle database integrity error (rollback and raise a 500 server error)
        db.rollback()
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while processing the transaction."
        )

    except Exception as e:
        # Catch all other exceptions
        db.rollback()
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.post(
    "/buygoods",
    status_code=status.HTTP_201_CREATED,
    response_model=transactions.ResponseTransact,
    tags=["transactions"],
    summary="Buy goods and services",
    description="Allows users to purchase goods and services using funds from their account, ensuring that all transactions adhere to account balance limits.",
    dependencies=[Depends(RateLimiter(times=1, seconds=60))]
)
def buygoods(
    transaction: transactions.Transaction,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Allows users to buy goods and services using funds from their bank accounts.
    
    The function performs the following steps:
    - Verifies if the requested transaction amount is valid (greater than zero).
    - Confirms the existence of the account and checks whether it has enough funds.
    - Deducts the transaction amount from the account balance if sufficient funds are available.
    - Generates a unique reference number for the transaction.
    - Logs the transaction and responds with the transaction details.
    
    Args:
        transaction (transactions.Transaction): The transaction payload containing the transaction details.
        db (Session): The database session, injected by FastAPI's dependency system.
        current_user (str): The authenticated user (obtained using OAuth), representing the user making the purchase.

    Returns:
        transactions.ResponseTransact: Details of the completed transaction (including the unique reference number and other metadata).

    Raises:
        HTTPException:
            - 404: If the account does not exist.
            - 400: If the transaction amount is invalid or insufficient.
            - 501: If funds are insufficient.
            - 500: For unexpected errors (e.g., database failures).
    """

    # Create the new buy goods transaction
    new_transaction = BuyGoods(
        id=uuid4(),
        ref_no=uuid4(),
        date_posted=datetime.now(),
        **transaction.payload,
        owner_customer_no=current_user.customer_no
    )
    
    # Try to find the account in either Personal or Corporate account classes
    account = None
    for clss in ACCOUNT_CLASSES:
        account = db.query(clss).filter(clss.account_no == transaction.payload['account']).first()
        if account:  # If account found, break loop
            break

    try:
        # Verify if account exists
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account does not exist."
            )
        
        # Ensure transaction amount is greater than zero
        if transaction.payload['amount'] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction amount must be greater than zero."
            )
        
        if account.account_type == "Personal Loan" or account.account_type == "Business Loan":
            if account.disposable_amount < transaction.payload['amount']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds for this transaction."
                )
            else:
                account.disposable_amount -= transaction.payload['amount']
        else:
            if account.account_balance < transaction.payload['amount']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds for this transaction."
                )
            else:
                 account.account_balance -= transaction.payload['amount']

        # Generate reference number for the transaction
        new_transaction.generate_ref_number()

        # Commit the transaction to the database
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        # Log the transaction for auditing
        logger.info(
            f"User {current_user} completed a purchase of {transaction.payload['amount']} "
            f"from account {transaction.payload['account']}."
        )

        # Return the transaction details
        return new_transaction

    except Exception as e:
        # Rollback the transaction in case of errors
        db.rollback()

        # Raise an internal server error for unexpected exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.post(
    "/paybill",
    status_code=status.HTTP_201_CREATED,
    response_model=transactions.ResponseTransact,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    tags=["transactions"],
    summary="Pay utility bills",
    description="Allows users to make payments for utility bills (e.g., electricity, water, or other services) "
                "using funds from their bank accounts while ensuring account balance sufficiency."
)
def paybill(
    transaction: transactions.Transaction,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Allows users to make utility bill payments using funds from their accounts.

    This endpoint facilitates paying utility bills (e.g., electricity, water) by verifying the account balance 
    and ensuring it is sufficient before allowing the transaction. The function also generates a reference number 
    for each successful transaction and logs the payment activity.

    Args:
        transaction (transactions.Transaction): The payload containing transaction details such as account,
                                                 amount, and other transaction-related data.
        db (Session): The SQLAlchemy session to interact with the database.
        current_user (str): The authenticated user making the transaction.

    Returns:
        transactions.ResponseTransact: Details of the transaction after processing, including reference number 
                                        and transaction status.
    
    Raises:
        HTTPException:
            - 404: If the account is not found.
            - 400: If the transaction amount is invalid.
            - 501: If there are insufficient funds in the account.
            - 500: For any unexpected errors during processing.
    """
    # Initialize new PayBill transaction
    new_transaction = PayBill(
        id=uuid4(),
        ref_no=uuid4(),
        **transaction.payload,
        date_posted=datetime.now(),
        owner_customer_no=current_user.customer_no
    )

    # Check account existence and balance sufficiency
    account = None
    for clss in ACCOUNT_CLASSES:
        account = db.query(clss).filter(clss.account_no == transaction.payload['account']).first()
        if account:  # Break out of loop once account is found
            break

    try:
        # Account existence check
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account does not exist."
            )

        if account.account_type == "Personal Loan" or account.account_type == "Business Loan":
            if account.disposable_amount < transaction.payload['amount']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds for this transaction."
                )
            else:
                account.disposable_amount -= transaction.payload['amount']
        else:
            if account.account_balance < transaction.payload['amount']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds for this transaction."
                )
            else:
                 account.account_balance -= transaction.payload['amount']

        # Generate the reference number for the transaction
        new_transaction.generate_ref_number()

        # Commit the transaction and persist it in the database
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        # Log the transaction for auditing purposes
        logger.info(
            f"User {current_user} made a bill payment of {transaction.payload['amount']} "
            f"from account {transaction.payload['account']}."
        )

        # Return the transaction details as a response
        return new_transaction

    except Exception as e:
        # Rollback the transaction in case of any error
        db.rollback()
        
        # Raise an internal server error with the specific exception details
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.post(
    "/airtime",
    status_code=status.HTTP_201_CREATED,
    response_model=transactions.ResponseTransact,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Transfer funds between accounts",
    description="Allows users to transfer funds from bank accounts to mobile accounts (MPESA, AIRTEL, Telcom) adhering to specified limits."
)
def buy_airtime(
    transaction: transactions.Transaction,
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
    for clss in ACCOUNT_CLASSES:
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
        if account.account_type == "Personal Loan" or account.account_type == "Business Loan":
            if account.disposable_amount < transaction.payload['amount']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds for this transaction."
                )
            else:
                account.disposable_amount -= transaction.payload['amount']
        else:
            if account.account_balance < transaction.payload['amount']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient funds for this transaction."
                )
            else:
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

@router.post(
    "/topup_wallet",
    status_code=status.HTTP_201_CREATED,
    response_model=transactions.ResponseTransact,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Transfer funds to a mobile wallet",
    description="Enables users to transfer funds from their bank accounts to mobile wallets like MPESA, Airtel, or Telcom, "
                "ensuring all transactions comply with account limits."
)
def topup_wallet(
    transaction: transactions.Transaction,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Facilitates transferring funds from a bank account to a mobile wallet.

    This endpoint handles the transfer of funds to mobile wallets (e.g., MPESA, Airtel, or Telcom) by validating
    account details and ensuring the user's account has sufficient funds. Each successful transaction is recorded
    with a unique reference number.

    Args:
        transaction (schemas.Transaction): The payload containing account and transaction details (e.g., amount, account number).
        db (Session): The database session to perform database operations.
        current_user (str): The authenticated user initiating the transaction.

    Returns:
        transactions.ResponseTransact: Details of the successful transaction, including a unique reference number.

    Raises:
        HTTPException:
            - 404: If the bank account doesn't exist.
            - 400: If the transaction amount is invalid or insufficient funds are available.
            - 500: For unexpected errors during processing.
    """
    # Initialize a new TopUpWallet transaction
    new_transaction = TopUpWallet(
        id=uuid4(),
        ref_no=uuid4(),
        date_posted=datetime.now(),
        **transaction.payload,
        owner_customer_no=current_user.customer_no
    )

    # Validate account existence
    account = None
    for clss in ACCOUNT_CLASSES:
        account = db.query(clss).filter(clss.account_no == transaction.payload['account']).first()
        if account:  # Exit loop as soon as account is found
            break

    try:
        # Account existence check
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account does not exist."
            )

        # Validate transaction amount
        if transaction.payload['amount'] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction amount must be greater than zero."
            )

        # Ensure sufficient funds
        if account.account_balance < transaction.payload['amount']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed. Insufficient funds."
            )

        # Deduct transaction amount from the account balance
        account.account_balance -= transaction.payload['amount']

        # Generate a unique reference number for the transaction
        new_transaction.generate_ref_number()

        # Persist the transaction in the database
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        # Log the transaction for auditing purposes
        logger.info(
            f"User {current_user} transferred {transaction.payload['amount']} "
            f"from account {transaction.payload['account']} to a mobile wallet."
        )

        # Return the transaction details as the response
        return new_transaction

    except Exception as e:
        # Rollback the transaction on any error
        db.rollback()

        # Log the exception
        logger.error(f"Error processing wallet top-up: {str(e)}")

        # Raise an internal server error exception
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )



@router.get(
    "/all_user_transactions",
    status_code=status.HTTP_200_OK,
    response_model=List[transactions.AllTransactions],
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
        topups = user.get_topups(db)

        # Consolidate all transactions
        all_transactions = c2b_transactions + bills + goods_and_services + airtime + topups

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