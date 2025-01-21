from fastapi import Depends, status, APIRouter, HTTPException, File, Form, UploadFile
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
import logging
from .. import schemas, oauth
from ..database import get_db
from ..models.accounts import PersonalAccounts, ForeignCurrency, CorporateAccounts
from typing import List
from ..models.files import Signatures, Signatory, CorporateDocs, PersonalDocs, F_C_A_Docs
import secrets
import os
import json


router = APIRouter(prefix="/post")
def save_prof(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    raw_fn = random_hex + f_ext
    return raw_fn

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
async def create_personal_account(
    payload: str = Form(...),
    signature: str = Form(...),
    tax_cert: UploadFile = File(...),
    reg_cert: UploadFile = File(...),
    passport: UploadFile = File(...),
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
    parsed_payload = schemas.PersonalAccount(**json.loads(payload))
    valid_account_types = ["Pay As You Go", "Savings Account", "Current Account"]
    # Validate the provided account type
    if parsed_payload.account_type not in valid_account_types:
        logger.warning(f"Invalid account type requested: {parsed_payload.account_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid account type. Allowed types are: {', '.join(valid_account_types)}."
        )

    existing_account = db.query(PersonalAccounts).filter(
        PersonalAccounts.owner_customer_no == current_user.customer_no,
        PersonalAccounts.account_type == parsed_payload.account_type
    ).first()
    if existing_account:
        if existing_account.account_name == parsed_payload.account_name:
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
        **parsed_payload.dict()
    )
    tax_filename = save_prof(tax_cert)
    reg_filename = save_prof(reg_cert)
    pass_filename = save_prof(passport)
    files = [tax_cert, reg_cert, passport]
    for file in files:
        filename = save_prof(file)
        file_location = f"uploads/account_documents/{filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
    taxcertificate = PersonalDocs(name=tax_filename, doc_type="tax-certificate", personal_account=account)
    bus_registration = PersonalDocs(name=reg_filename, doc_type="national-id", personal_account=account)
    passport = PersonalDocs(name=pass_filename, doc_type="passport-photo", personal_account=account)

    try:
        db.add_all([taxcertificate, bus_registration, passport, account])
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
async def create_foreign_currency_account(
    payload: str = Form(...),
    signature: str = Form(...),
    utility: UploadFile = File(...),
    reg_cert: UploadFile = File(...),
    passport: UploadFile = File(...),
    salary_slip: UploadFile = File(...),
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
    parsed_payload = schemas.ForeignCurrencyAccount(**json.loads(payload))
    # Define allowed account type
    valid_account_types = ["Forex Plus", "Forex Advantage", "Forex Go"]

    # Validate the account type
    if parsed_payload.account_type not in valid_account_types:
        logger.warning(f"Invalid account type requested: {parsed_payload.account_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid account type. Allowed types are: {', '.join(valid_account_types)}."
        )

    existing_account = db.query(ForeignCurrency).filter(
        ForeignCurrency.owner_customer_no == current_user.customer_no,
        ForeignCurrency.account_type == parsed_payload.account_type
    ).first()
    if existing_account:
        if existing_account.account_name == parsed_payload.account_name:
            logger.info(f"Account creation conflict for user {current_user.customer_no}.")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account of this type already exists for the user."
            )

    # Generate account and save to the database
    account = ForeignCurrency(
        owner_customer_no=current_user.customer_no,
        account_no=str(uuid4()),
        **parsed_payload.dict()
    )
    account.update_balance()
    utility_filename = save_prof(utility)
    reg_filename = save_prof(reg_cert)
    pass_filename = save_prof(passport)
    salary_slip_filename = save_prof(salary_slip)
    files = [utility, reg_cert, passport, salary_slip]
    for file in files:
        filename = save_prof(file)
        file_location = f"uploads/account_documents/{filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
    utility_receipt = F_C_A_Docs(name=utility_filename, doc_type="utility_receipt", foreign_currency_account=account)
    bus_registration = F_C_A_Docs(name=reg_filename, doc_type="national-id", foreign_currency_account=account)
    pass_port = F_C_A_Docs(name=pass_filename, doc_type="passport-photo", foreign_currency_account=account)
    salaryslip = F_C_A_Docs(name=salary_slip_filename, doc_type="salary-slip", foreign_currency_account=account)
    try:
        db.add_all([utility_receipt, bus_registration, pass_port, account, salaryslip])
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
@router.post("/open_corporate_account",
response_model=schemas.ResponseAccount,
summary="Create a new corporate account",
description="Allows authenticated users to create a new corporate account. Each account is assigned a unique account number, "
            "is associated with the current user, and is validated to ensure compliance with account type restrictions.")
async def create_corporate_account(
    payload: str = Form(...),
    signature: str = Form(...),
    tax_cert: UploadFile = File(...),
    reg_cert: UploadFile = File(...),
    passport: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    parsed_payload = schemas.CorporateAccount(**json.loads(payload))
    valid_account_types = ["Vue Vantage", "SME Banking", "Vue Corporate"]
    # Validate the provided account type
    if parsed_payload.account_type not in valid_account_types:
        logger.warning(f"Invalid account type requested: {parsed_payload.account_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid account type. Allowed types are: {', '.join(valid_account_types)}."
        )

    # Generate account and save to the database
    account = CorporateAccounts(
        owner_customer_no=current_user.customer_no,
        account_balance = 50000.00,
        account_no=str(uuid4()),
        **parsed_payload.dict()
    )
    tax_filename = save_prof(tax_cert)
    reg_filename = save_prof(reg_cert)
    pass_filename = save_prof(passport)
    files = [tax_cert, reg_cert, passport]
    for file in files:
        filename = save_prof(file)
        file_location = f"uploads/account_documents/{filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
    taxcertificate = CorporateDocs(name=tax_filename, doc_type="tax-certificate", personal_account=account)
    bus_registration = CorporateDocs(name=reg_filename, doc_type="registration-id", personal_account=account)
    passport = CorporateDocs(name=pass_filename, doc_type="passport-photo", personal_account=account)

    try:
        db.add_all([taxcertificate, bus_registration, passport, account])
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
    response_model=List[schemas.ResponseAccount2]
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
    for account in accounts:
        account.truncate_uuid()
        account.format_cash()
    return accounts


@router.get(
    "/get_user_transactive_accounts",
    status_code=status.HTTP_200_OK, 
    response_model=List[schemas.ResponseAccount1]
)
def get_user_transactive_accounts(
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
    personal_accounts = db.query(PersonalAccounts).filter(
        PersonalAccounts.owner_customer_no == current_user.customer_no,
    ).all()
    corporate_accounts = db.query(CorporateAccounts).filter(
        CorporateAccounts.owner_customer_no == current_user.customer_no
    ).all()

    accounts = personal_accounts + corporate_accounts
    return accounts

@router.get(
    "/get_user_savings_accounts", 
    status_code=status.HTTP_200_OK, 
    response_model=List[schemas.ResponseAccount2]
)
def get_user_savings_accounts(
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
        PersonalAccounts.owner_customer_no == current_user.customer_no,
        PersonalAccounts.account_type == "Savings Account"
    ).all()
    for account in accounts:
        account.truncate_uuid()
        account.format_cash()
    return accounts

@router.get(
    "/get_user_current_accounts",
    status_code=status.HTTP_200_OK, 
    response_model=List[schemas.ResponseAccount2]
)
def get_user_current_accounts(
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
    personal_accounts = db.query(PersonalAccounts).filter(
        PersonalAccounts.owner_customer_no == current_user.customer_no,
        PersonalAccounts.account_type != "Savings Account"
    ).all()
    corporate_accounts = db.query(CorporateAccounts).filter(
        CorporateAccounts.owner_customer_no == current_user.customer_no
    ).all()
    accounts = personal_accounts + corporate_accounts
    for account in accounts:
        account.truncate_uuid()
        account.format_cash()
    return accounts