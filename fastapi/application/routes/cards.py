from fastapi import  Depends, status, APIRouter, HTTPException, status
from .. import schemas, oauth
from ..models.cards import BaseCards, DebitCards, CreditCards, PrepaidCards
from ..models.accounts import Account
from datetime import datetime
from ..database import  get_db
from sqlalchemy.orm import Session
from uuid import uuid4
import logging
from typing import List
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/post")

@router.post(
    "/debit_card_application",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CardApplicationResponse,
    summary="Apply for a debit card",
    description="This endpoint allows authenticated users to apply for a new debit card. The application includes generating a card number, setting issuance and expiry dates, and associating it with the current user."
)
def apply_debit_card(
    new_card: schemas.CardApplication,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Apply for a debit card.

    This endpoint allows authenticated users to apply for a new debit card. The card details, including
    the card number, issuance date, expiry date, and owner information, are automatically generated and 
    stored in the database.

    Args:
        new_card (schemas.CardApplication): The payload containing debit card application details.
        db (Session): The database session for executing queries.
        current_user (str): The authenticated user making the request.

    Returns:
        schemas.CardApplicationResponse: The details of the successfully created debit card application.

    Raises:
        HTTPException: If an error occurs during the process of creating the application.
    """
    # Generate card details
    try:
        card_no = BaseCards.generate_card_no()
    except Exception as e:
        logger.error(f"Error generating card number: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate card number."
        )

    # Create new debit card application
    request = DebitCards(
        card_no=card_no,
        date_issued=datetime.now(),
        expiry_date=datetime.now() + relativedelta(years=3),
        date_requested=datetime.now(),
        owner_customer_no=current_user.customer_no,
        id=str(uuid4()),
        **new_card.payload
    )

    try:
        db.add(request)
        db.commit()
        db.refresh(request)
        logger.info(f"Debit card application created successfully for user {current_user.customer_no}")
        return request
    except Exception as e:
        logger.error(f"Error processing debit card application for user {current_user.customer_no}: {e}")
        db.rollback()  # Ensure transaction consistency
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process debit card application."
        )
    finally:
        db.close()


@router.post(
    "/credit_card_application",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CardApplicationResponse,
    summary="Apply for a credit card",
    description="This endpoint allows authenticated users to apply for a new credit card, generating a unique card number, "
                "and associating it with the current user. The card has a default expiry of one year."
)
def apply_credit_card(
    new_card: schemas.CardApplication,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Apply for a credit card.

    This endpoint creates a new credit card application for an authenticated user. 
    A unique card number is generated, and the application includes relevant details such as 
    issue date, expiry date, and due date.

    Args:
        new_card (schemas.CardApplication): The payload containing credit card application details.
        db (Session): The database session for executing queries.
        current_user (str): The authenticated user making the request.

    Returns:
        schemas.CardApplicationResponse: The details of the successfully created credit card application.

    Raises:
        HTTPException: If an error occurs during the application process.
    """
    # Generate card application
    request = CreditCards(
        card_no=BaseCards.generate_card_no(),
        date_issued=datetime.now(),
        expiry_date=datetime.now() + relativedelta(years=1),
        date_requested=datetime.now(),
        owner_customer_no=current_user.customer_no,
        due_date=datetime.now(),
        id=str(uuid4()),
        **new_card.payload
    )

    try:
        db.add(request)
        db.commit()
        db.refresh(request)
        logger.info(f"Credit card application successfully created for user {current_user.customer_no}")
        return request
    except Exception as e:
        logger.error(f"Failed to process credit card application for user {current_user.customer_no}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process credit card application."
        )
    finally:
        db.close()

#
@router.post(
    "/prepaid_card_application",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CardApplicationResponse,
    summary="Apply for a prepaid card",
    description="This endpoint allows authenticated users to apply for a new prepaid card. It debits the specified "
                "account for the card's initial balance and associates the card with the user."
)
def apply_prepaid_card(
    new_card: schemas.CardApplication,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Apply for a prepaid card.

    This endpoint creates a prepaid card application for an authenticated user. It generates a unique card number,
    deducts the initial balance from the specified account, and saves the card details to the database.

    Args:
        new_card (schemas.CardApplication): The payload containing prepaid card application details, including account number and balance.
        db (Session): The database session for executing queries.
        current_user (str): The authenticated user making the request.

    Returns:
        schemas.CardApplicationResponse: The details of the successfully created prepaid card application.

    Raises:
        HTTPException: If the account is invalid, insufficient funds are available, or an error occurs during processing.
    """
    account_to_debit = db.query(Account).filter(
        Account.account_no == new_card.payload['account_number']
    ).first()

    # Validate account existence and balance
    if not account_to_debit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found for the specified account number."
        )
    if account_to_debit.account_balance < new_card.payload['balance']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds in the specified account."
        )

    # Deduct balance and generate prepaid card
    account_to_debit.account_balance -= new_card.payload['balance']
    del new_card.payload['account_number']  # Clean payload before creating the card
    request = PrepaidCards(
        card_no=BaseCards.generate_card_no(),
        date_issued=datetime.now(),
        expiry_date=datetime.now() + relativedelta(years=1),
        date_requested=datetime.now(),
        owner_customer_no=current_user.customer_no,
        id=str(uuid4()),
        **new_card.payload
    )

    try:
        db.add(request)
        db.commit()
        db.refresh(request)
        logger.info(f"Prepaid card application successfully created for user {current_user.customer_no}")
        return request
    except Exception as e:
        logger.error(f"Failed to process prepaid card application for user {current_user.customer_no}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process prepaid card application."
        )
    finally:
        db.close()


@router.get(
    "/get_user_debit_cards", 
    status_code=status.HTTP_200_OK, 
    response_model=List[schemas.GetDebitCards],
    summary="Retrieve user's debit cards",
    description="Fetch all debit cards associated with the current authenticated user. Card numbers are obfuscated, "
                "UUIDs are truncated, and date fields are formatted for readability."
)
def get_user_debit_cards(
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Retrieve user's debit cards.

    Fetches all debit cards associated with the current authenticated user. The card number is partially obfuscated, 
    UUIDs are truncated, and datetime fields are formatted for improved readability. The date issued is printed 
    for reference.

    Args:
        db (Session): The database session for executing queries.
        current_user (str): The authenticated user making the request.

    Returns:
        List[schemas.GetDebitCards]: A list of debit card details for the authenticated user.

    Raises:
        HTTPException: If an error occurs during data retrieval.
    """
    try:
        # Fetch user debit cards
        accounts = db.query(DebitCards).filter(
            DebitCards.owner_customer_no == current_user.customer_no
        ).all()

        for account in accounts:
            account.reformat_card_no()  # Obfuscate card number
            account.truncate_uuid()  # Truncate UUID
            account.truncate_datetime()  # Truncate datetime fields

        return accounts
    except Exception as e:
        logger.error(f"Error fetching debit cards for user {current_user.customer_no}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve debit cards."
        )
    finally:
        db.close()


@router.get(
    "/get_user_credit_cards", 
    status_code=status.HTTP_200_OK, 
    response_model=List[schemas.GetCreditCards],
    summary="Retrieve user's credit cards",
    description="Fetch all credit cards associated with the current authenticated user. The card number is partially "
                "obfuscated, and the date fields are truncated for improved readability."
)
def get_user_credit_cards(
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Retrieve user's credit cards.

    Fetches all credit cards associated with the current authenticated user. The card number is partially obfuscated, 
    and datetime fields are truncated for improved readability.

    Args:
        db (Session): The database session for executing queries.
        current_user (str): The authenticated user making the request.

    Returns:
        List[schemas.GetCreditCards]: A list of credit card details for the authenticated user.

    Raises:
        HTTPException: If an unexpected error occurs during data retrieval.
    """
    try:
        # Fetch user credit cards
        accounts = db.query(CreditCards).filter(
            CreditCards.owner_customer_no == current_user.customer_no
        ).all()

        for account in accounts:
            account.reformat_card_no()  # Obfuscate card number
            account.truncate_datetime()  # Truncate datetime fields

        return accounts
    except Exception as e:
        logger.error(f"Error fetching credit cards for user {current_user.customer_no}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve credit cards."
        )
    finally:
        db.close()


@router.get(
    "/get_user_prepaid_cards", 
    status_code=status.HTTP_200_OK, 
    response_model=List[schemas.GetPrepaidCards],
    summary="Retrieve user's prepaid cards",
    description="Fetch all prepaid cards associated with the current authenticated user. The card number is partially "
                "obfuscated, and the date fields are truncated for improved readability."
)
def get_user_prepaid_cards(
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Retrieve user's prepaid cards.

    Fetches all prepaid cards associated with the current authenticated user. The card number is partially obfuscated, 
    and datetime fields are truncated for improved readability.

    Args:
        db (Session): The database session for executing queries.
        current_user (str): The authenticated user making the request.

    Returns:
        List[schemas.GetPrepaidCards]: A list of prepaid card details for the authenticated user.

    Raises:
        HTTPException: If an unexpected error occurs during data retrieval.
    """
    try:
        # Fetch user prepaid cards
        accounts = db.query(PrepaidCards).filter(
            PrepaidCards.owner_customer_no == current_user.customer_no
        ).all()

        for account in accounts:
            account.reformat_card_no()  # Obfuscate card number
            account.truncate_datetime()  # Truncate datetime fields

        return accounts
    except Exception as e:
        logger.error(f"Error fetching prepaid cards for user {current_user.customer_no}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve prepaid cards."
        )
    finally:
        db.close()
