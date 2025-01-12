from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
import logging
from .. import schemas, oauth
from ..database import get_db
from ..models.accounts import PersonalAccounts, ForeignCurrency, CorporateAccounts

router = APIRouter(prefix="/post")
logger = logging.getLogger(__name__)

@router.post(
    "/open_personal_account",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseAccount,
    summary="Create a new personal account",
    description="Allows authenticated users to create a new personal account. Each account is uniquely identified, "
                "associated with the current user, and validated to ensure compliance with account type restrictions."
)
def create_personal_account(
    new_account: schemas.Account,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Create a new personal account for the authenticated user.

    This endpoint facilitates the creation of a new personal account. The account is assigned a unique identifier, 
    and users can only create one account per account type. Valid account types include "Pay As You Go", 
    "Savings Accountl", and "Current Account".

    Args:
        new_account (schemas.Account): The account details provided by the user.
        db (Session): The database session used for database operations.
        current_user (str): The current authenticated user making the request.

    Returns:
        schemas.ResponseAccount: Details of the newly created account.

    Raises:
        HTTPException:
            - 400: If the account type is invalid.
            - 409: If the user already has an account of the specified type.
            - 500: If an unexpected error occurs while processing the request.
    """
    valid_account_types = ["Pay As You Go", "Savings Account", "Current Account"]

    # Validate the provided account type
    if new_account.payload['account_type'] not in valid_account_types:
        logger.warning(f"Invalid account type requested: {new_account.payload['account_type']}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid account type. Allowed types are: {', '.join(valid_account_types)}."
        )

    # Check if the user already has an account of the specified type
    existing_account = db.query(PersonalAccounts).filter(
        PersonalAccounts.owner_customer_no == current_user.customer_no,
        PersonalAccounts.account_type == new_account.payload['account_type']
    ).first()

    if existing_account:
        logger.info(f"Account creation conflict for user {current_user.customer_no}.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account of this type already exists for the user."
        )

    # Generate account and save to the database
    account = PersonalAccounts(
        owner_customer_no=current_user.customer_no,
        account_balance = 50000.00,
        account_no=str(uuid4()),
        **new_account.payload
    )

    try:
        db.add(account)
        db.commit()
        db.refresh(account)
        logger.info(f"Account created successfully for user {current_user.customer_no}.")
        return account
    except Exception as e:
        logger.error(f"Error creating account for user {current_user.customer_no}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the account."
        )




@router.get(
    "/get_user_personal_accounts", 
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
    accounts = db.query(PersonalAccounts).filter(
        PersonalAccounts.owner_customer_no == current_user.customer_no
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
    accounts = db.query(PersonalAccounts).filter(
        PersonalAccounts.owner_customer_no == current_user.customer_no,
        PersonalAccounts.account_type.in_(["Pay As You Go", "Savings Account"])
    ).all()
    return accounts

@router.post(
    "/open_corporate_account",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseAccount,
    summary="Create a new corporate account",
    description="Allows authenticated users to create a new corporate account. Each account is assigned a unique account number, "
                "is associated with the current user, and is validated to ensure compliance with account type restrictions."
)
def create_corporate_account(
    new_account: schemas.Account,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Create a new corporate account for the authenticated user.

    This endpoint facilitates the creation of a corporate account tied to the current user. 
    Corporate accounts can only be of specific types, and users are restricted to one account per type.

    Args:
        new_account (schemas.Account): The details of the corporate account to be created.
        db (Session): The database session for performing database operations.
        current_user (str): The authenticated user making the request.

    Returns:
        schemas.ResponseAccount: Details of the newly created corporate account.

    Raises:
        HTTPException:
            - 400: If the provided account type is invalid.
            - 409: If a corporate account of this type already exists for the user.
            - 500: If an unexpected error occurs during the account creation process.
    """
    # Define valid corporate account types
    valid_account_types = ["Mortgage", "Car Loan", "General Loan"]

    # Validate account type
    if new_account.account_type not in valid_account_types:
        logger.warning(f"Invalid corporate account type requested: {new_account.account_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid account type. Allowed types: {', '.join(valid_account_types)}"
        )

    # Check if the user already has an account of this type
    existing_account = db.query(CorporateAccounts).filter(
        CorporateAccounts.owner_customer_no == current_user.customer_no,
        CorporateAccounts.account_type == new_account.account_type
    ).first()

    if existing_account:
        logger.info(f"Corporate account creation conflict for user {current_user.customer_no}.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A corporate account of this type already exists for the user."
        )

    # Create a new corporate account
    account = CorporateAccounts(
        owner_customer_no=current_user.customer_no,
        account_no=str(uuid4()),  # Generate unique account number
        **new_account.dict()
    )

    try:
        db.add(account)
        db.commit()
        db.refresh(account)
        logger.info(f"Corporate account created successfully for user {current_user.customer_no}.")
        return account
    except Exception as e:
        logger.error(f"Error creating corporate account for user {current_user.customer_no}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the corporate account."
        )


@router.post(
    "/open_foreign_currency_account",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseAccount,
    summary="Create a new foreign currency account",
    description=(
        "This endpoint allows authenticated users to create a new foreign currency account. "
        "Each account is assigned a unique account number, linked to the current user, and supports foreign currencies."
    )
)
def create_foreign_currency_account(
    new_account: schemas.Account,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Create a new foreign currency account for the authenticated user.

    This endpoint allows users to open a foreign currency account associated with their profile.
    Accounts are restricted to a predefined type (`Forex Plus`) and are created in the specified currency.

    Args:
        new_account (schemas.Account): The details of the account to be created.
        db (Session): The database session used for performing database operations.
        current_user (str): The authenticated user making the request.

    Returns:
        schemas.ResponseAccount: Details of the newly created foreign currency account.

    Raises:
        HTTPException:
            - 400: If the provided account type is invalid.
            - 409: If a foreign currency account of this type already exists for the user.
            - 500: If an unexpected error occurs during account creation.
    """
    # Define allowed account type
    valid_account_types = ["Forex Plus"]

    # Validate the account type
    if new_account.account_type not in valid_account_types:
        logger.warning(f"Invalid foreign currency account type requested: {new_account.account_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid account type. Allowed types: {', '.join(valid_account_types)}"
        )

    # Check if the account already exists for this user and type
    existing_account = db.query(ForeignCurrency).filter(
        ForeignCurrency.owner_customer_no == current_user.customer_no,
        ForeignCurrency.account_type == new_account.account_type
    ).first()

    if existing_account:
        logger.info(f"Conflict: Foreign currency account already exists for user {current_user.customer_no}.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A foreign currency account of this type already exists for the user."
        )

    # Create a new foreign currency account
    account = models.ForeignCurrency(
        owner_customer_no=current_user.customer_no,
        currency="USD",  # Set a default currency; modify as necessary for multi-currency support
        account_no=str(uuid4()),  # Unique account number
        **new_account.dict()
    )

    # Update the initial account balance
    account.update_balance()

    try:
        db.add(account)
        db.commit()
        db.refresh(account)
        logger.info(f"Foreign currency account created successfully for user {current_user.customer_no}.")
        return account
    except Exception as e:
        logger.error(f"Error creating foreign currency account for user {current_user.customer_no}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the foreign currency account."
        )


