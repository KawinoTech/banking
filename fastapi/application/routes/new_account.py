from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
import logging
from .. import models, schemas, oauth
from ..database import get_db

router = APIRouter(prefix="/post")
logger = logging.getLogger(__name__)

@router.post(
    "/open_new_account",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseAccount,
    summary="Create a new user account",
    description="This endpoint allows authenticated users to create a new account. Each account is assigned a unique account number and associated with the current user."
)
def create_account(
    new_account: schemas.Account,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Create a new account for the authenticated user.

    This endpoint facilitates the creation of a new account tied to the current user. 
    The account number is automatically generated and validated before creation.

    Args:
        new_account (schemas.Account): The account details provided by the user.
        db (Session): The database session used for database interactions.
        current_user (str): The currently authenticated user.

    Returns:
        schemas.ResponseAccount: The newly created account details.

    Raises:
        HTTPException: If the account already exists or an error occurs during the creation process.
    """
    # Validate account type and ensure account doesn't already exist
    valid_account_types = ["Pay As You Go", "Savings Account", "Current Account"]
    if new_account.account_type not in valid_account_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid account type. Allowed types: {', '.join(valid_account_types)}"
        )

    # Check if the user already has an account of the same type
    existing_account = db.query(models.Account).filter(
        models.Account.owner_customer_no == current_user.customer_no,
        models.Account.account_type == new_account.account_type
    ).first()

    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account of this type already exists for the user."
        )

    # Create a new account
    account = models.Account(
        owner_customer_no=current_user.customer_no,
        account_no=str(uuid4()),
        **new_account.dict()
    )

    try:
        db.add(account)
        db.commit()
        db.refresh(account)
        return account
    except Exception as e:
        # Proper logging for debugging
        logger.error(f"Error creating account for user {current_user.customer_no}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the account."
        )



@router.get(
    "/get_user_accounts", 
    status_code=status.HTTP_200_OK, 
    response_model=List[schemas.ResponseAccount1]
)
def get_user_accounts(
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
    accounts = db.query(models.Account).filter(
        models.Account.owner_customer_no == current_user.customer_no
    ).all()
    return accounts


@router.get(
    "/get_user_current&savings_accounts", 
    status_code=status.HTTP_200_OK, 
    response_model=List[schemas.ResponseAccount1]
)
def get_user_current_and_savings_accounts(
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
    accounts = db.query(models.Account).filter(
        models.Account.owner_customer_no == current_user.customer_no,
        models.Account.account_type.in_(["Pay As You Go", "Savings Account"])
    ).all()
    return accounts
