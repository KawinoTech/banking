from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
from typing import List
from dateutil.relativedelta import relativedelta
import logging

from .. import oauth
from ..models.cards import BaseCards, DebitCards, CreditCards, PrepaidCards
from ..models.accounts import PersonalAccounts
from ..database import get_db
from ..schema import cards

# Set up the logger
logger = logging.getLogger(__name__)

# Set up the router
router = APIRouter(
    prefix="/post",
    tags=["Card Services"],  # Group these endpoints under the "Card Services" category in the API docs
)

@router.post(
    "/debit_card_application",
    status_code=status.HTTP_201_CREATED,
    response_model=cards.CardApplicationResponse,
    summary="Apply for a debit card",
    description=(
        "This endpoint allows authenticated users to apply for a new debit card. "
        "The application includes generating a card number, setting issuance and expiry dates, "
        "and associating it with the current user."
    ),
)
def apply_debit_card(
    new_card: cards.CardApplication,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Apply for a debit card.

    This endpoint generates a new debit card application for authenticated users. It assigns 
    a unique card number, sets issuance and expiry dates, and associates the card with the 
    requesting user.

    Args:
        new_card (cards.CardApplication): The payload containing debit card application details.
        db (Session): The database session for executing queries.
        current_user (str): The authenticated user making the request.

    Returns:
        cards.CardApplicationResponse: The details of the successfully created debit card.

    Raises:
        HTTPException: If an error occurs during card number generation or database operations.
    """
    logger.info("Processing debit card application...")

    # Step 1: Generate a card number
    try:
        card_no = BaseCards.generate_card_no()
        logger.debug(f"Generated card number: {card_no}")
    except Exception as e:
        logger.error(f"Failed to generate card number: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the card number.",
        )

    # Step 2: Validate the associated account and create the debit card application
    try:
        # Check if the attached account exists in the database
        account = db.query(PersonalAccounts).filter(
            PersonalAccounts.account_no == new_card.payload['account_attached_no']
        ).first()

        if not account:
            logger.warning(f"Account {new_card.payload['account_attached_no']} not found for user {current_user.customer_no}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account {new_card.payload['account_attached_no']} does not exist.",
            )

        # Create a new debit card application
        request = DebitCards(
            card_no=card_no,
            date_issued=datetime.now(),
            expiry_date=datetime.now() + relativedelta(years=3),
            date_requested=datetime.now(),
            personal_account=account,
            owner_customer_no=current_user.customer_no,
            id=str(uuid4()),
            **new_card.payload,
        )
        db.add(request)
        db.commit()
        db.refresh(request)

        logger.info(f"Debit card application created successfully for user {current_user.customer_no}")
        return request
    except HTTPException:
        raise  # Re-raise known exceptions
    except Exception as e:
        logger.error(f"Error creating debit card application for user {current_user.customer_no}: {e}")
        db.rollback()  # Roll back the transaction to ensure database consistency
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process the debit card application. Please try again later.",
        )

@router.post(
    "/credit_card_application",
    status_code=status.HTTP_201_CREATED,
    response_model=cards.CardApplicationResponse,
    summary="Apply for a credit card",
    description=(
        "This endpoint allows authenticated users to apply for a new credit card. "
        "A unique card number is generated, and the card is associated with the current user. "
        "The card has a default expiry of one year."
    ),
)
def apply_credit_card(
    new_card: cards.CardApplication,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Apply for a credit card.

    This endpoint creates a new credit card application for an authenticated user. 
    A unique card number is generated, and the application includes relevant details such as 
    issue date, expiry date, and due date.

    Args:
        new_card (cards.CardApplication): The payload containing credit card application details.
        db (Session): The database session for executing queries.
        current_user (str): The authenticated user making the request.

    Returns:
        cards.CardApplicationResponse: The details of the successfully created credit card.

    Raises:
        HTTPException: If an error occurs during the application process.
    """
    logger.info("Processing credit card application...")

    # Step 1: Generate a card number
    try:
        card_no = BaseCards.generate_card_no()
        logger.debug(f"Generated card number: {card_no}")
    except Exception as e:
        logger.error(f"Failed to generate card number: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the card number."
        )

    # Step 2: Create the credit card application
    try:
        request = CreditCards(
            card_no=card_no,
            date_issued=datetime.now(),
            expiry_date=datetime.now() + relativedelta(years=1),
            date_requested=datetime.now(),
            owner_customer_no=current_user.customer_no,
            due_date=datetime.now(),  # Optional: Add logic if `due_date` has a specific meaning
            id=str(uuid4()),
            **new_card.payload,
        )

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
            detail="Failed to process the credit card application. Please try again later.",
        )

@router.post(
    "/prepaid_card_application",
    status_code=status.HTTP_201_CREATED,
    response_model=cards.CardApplicationResponse,
    summary="Apply for a prepaid card",
    description=(
        "This endpoint allows authenticated users to apply for a new prepaid card. "
        "It debits the specified account for the card's initial balance and associates the card with the user."
    ),
)
def apply_prepaid_card(
    new_card: cards.CardApplication,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user),
):
    """
    Apply for a prepaid card.

    This endpoint creates a prepaid card application for an authenticated user. It generates a unique card number,
    deducts the initial balance from the specified account, and saves the card details to the database.

    Args:
        new_card (cards.CardApplication): The payload containing prepaid card application details,
            including account number and initial balance.
        db (Session): The database session for executing queries.
        current_user (str): The authenticated user making the request.

    Returns:
        cards.CardApplicationResponse: The details of the successfully created prepaid card.

    Raises:
        HTTPException: If the account is invalid, insufficient funds are available, 
        or an error occurs during processing.
    """
    logger.info("Initiating prepaid card application process...")

    # Step 1: Fetch and validate the account
    account_to_debit = db.query(PersonalAccounts).filter(
        PersonalAccounts.account_no == new_card.payload['account_number']
    ).first()

    if not account_to_debit:
        logger.error("Account not found for account number: %s", new_card.payload['account_number'])
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found for the specified account number.",
        )

    if account_to_debit.account_balance < new_card.payload['balance']:
        logger.error(
            "Insufficient funds for account number: %s, Requested: %s, Available: %s",
            new_card.payload['account_number'],
            new_card.payload['balance'],
            account_to_debit.account_balance,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds in the specified account.",
        )

    # Step 2: Deduct balance
    account_to_debit.account_balance -= new_card.payload['balance']

    # Step 3: Generate and create the prepaid card
    try:
        card_no = BaseCards.generate_card_no()
        logger.debug(f"Generated card number: {card_no}")

        del new_card.payload['account_number']  # Remove account number from payload as it's no longer needed
        prepaid_card = PrepaidCards(
            card_no=card_no,
            date_issued=datetime.now(),
            expiry_date=datetime.now() + relativedelta(years=1),
            date_requested=datetime.now(),
            owner_customer_no=current_user.customer_no,
            id=str(uuid4()),
            **new_card.payload,
        )

        db.add(prepaid_card)
        db.commit()
        db.refresh(prepaid_card)

        logger.info(f"Prepaid card application successfully created for user {current_user.customer_no}")
        return prepaid_card
    except Exception as e:
        logger.error(f"Failed to process prepaid card application for user {current_user.customer_no}: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process prepaid card application. Please try again later.",
        )


@router.get(
    "/get_user_debit_cards",
    status_code=status.HTTP_200_OK,
    response_model=List[cards.GetDebitCards],
    summary="Retrieve user's debit cards",
    description=(
        "Fetch all debit cards associated with the authenticated user. Card numbers are obfuscated, UUIDs are "
        "truncated, and date fields are formatted for readability."
    ),
)
def get_user_debit_cards(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user),
):
    """
    Retrieve user's debit cards.

    Fetch all debit cards associated with the current authenticated user. Card details include obfuscated card numbers,
    truncated UUIDs, and formatted datetime fields for improved readability.

    Args:
        db (Session): Database session for executing queries.
        current_user (str): The authenticated user making the request.

    Returns:
        List[schemas.GetDebitCards]: Debit card details for the authenticated user.

    Raises:
        HTTPException: If data retrieval fails.
    """
    logger.info("Fetching debit cards for user %s", current_user.customer_no)
    try:
        # Query and process debit cards
        debit_cards = db.query(DebitCards).filter(
            DebitCards.owner_customer_no == current_user.customer_no
        ).all()

        for card in debit_cards:
            card.reformat_card_no()  # Obfuscate card number
            card.truncate_uuid()  # Truncate UUID
            card.truncate_datetime()  # Format datetime fields

        return debit_cards
    except Exception as e:
        logger.error(f"Error fetching debit cards for user {current_user.customer_no}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve debit cards.",
        )


@router.get(
    "/get_user_credit_cards",
    status_code=status.HTTP_200_OK,
    response_model=List[cards.GetCreditCards],
    summary="Retrieve user's credit cards",
    description=(
        "Fetch all credit cards associated with the authenticated user. Card numbers are obfuscated, and date fields "
        "are formatted for readability."
    ),
)
def get_user_credit_cards(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user),
):
    """
    Retrieve user's credit cards.

    Fetch all credit cards associated with the current authenticated user. Card details include obfuscated card numbers
    and formatted datetime fields for improved readability.

    Args:
        db (Session): Database session for executing queries.
        current_user (str): The authenticated user making the request.

    Returns:
        List[schemas.GetCreditCards]: Credit card details for the authenticated user.

    Raises:
        HTTPException: If data retrieval fails.
    """
    logger.info("Fetching credit cards for user %s", current_user.customer_no)
    try:
        # Query and process credit cards
        credit_cards = db.query(CreditCards).filter(
            CreditCards.owner_customer_no == current_user.customer_no
        ).all()

        for card in credit_cards:
            card.reformat_card_no()  # Obfuscate card number
            card.truncate_datetime()  # Format datetime fields

        return credit_cards
    except Exception as e:
        logger.error(f"Error fetching credit cards for user {current_user.customer_no}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve credit cards.",
        )


@router.get(
    "/get_user_prepaid_cards",
    status_code=status.HTTP_200_OK,
    response_model=List[cards.GetPrepaidCards],
    summary="Retrieve user's prepaid cards",
    description=(
        "Fetch all prepaid cards associated with the authenticated user. Card numbers are obfuscated, and date fields "
        "are formatted for readability."
    ),
)
def get_user_prepaid_cards(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth.get_current_user),
):
    """
    Retrieve user's prepaid cards.

    Fetch all prepaid cards associated with the current authenticated user. Card details include obfuscated card numbers
    and formatted datetime fields for improved readability.

    Args:
        db (Session): Database session for executing queries.
        current_user (str): The authenticated user making the request.

    Returns:
        List[schemas.GetPrepaidCards]: Prepaid card details for the authenticated user.

    Raises:
        HTTPException: If data retrieval fails.
    """
    logger.info("Fetching prepaid cards for user %s", current_user.customer_no)
    try:
        # Query and process prepaid cards
        prepaid_cards = db.query(PrepaidCards).filter(
            PrepaidCards.owner_customer_no == current_user.customer_no
        ).all()

        for card in prepaid_cards:
            card.reformat_card_no()  # Obfuscate card number
            card.truncate_datetime()  # Format datetime fields

        return prepaid_cards
    except Exception as e:
        logger.error(f"Error fetching prepaid cards for user {current_user.customer_no}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve prepaid cards.",
        )

