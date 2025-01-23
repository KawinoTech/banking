from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
from ..schema import help_desk

from .. import schemas, oauth
from ..models.customer_service import ClientHelpRequest, ClientReports
from ..database import get_db

# Set up router with a specific prefix for related endpoints
router = APIRouter(
    prefix="/post",
    tags=["Customer Support"],  # Assign this router to a specific documentation category
)

@router.post(
    "/request_help",
    status_code=status.HTTP_201_CREATED,
    response_model=help_desk.ResponseHelp,
    summary="Submit a Help Request",
    description=(
        "This endpoint allows authenticated users to submit a request for help. "
        "It captures details such as the request text and links it to the user account. "
        "The created request is stored in the database for processing by customer service agents."
    ),
    responses={
        201: {"description": "Help request created successfully."},
        401: {"description": "Unauthorized. Access token is missing or invalid."},
        501: {"description": "Internal server error. Unable to save the request."},
    },
)
def request_help(
    new_request: help_desk.HelpDesk, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Handles requests for customer help.

    Parameters:
    - new_request (schemas.HelpDesk): Data submitted by the user for requesting help.
    - db (Session): Database session dependency.
    - current_user (str): Current authenticated user obtained from the oauth dependency.

    Returns:
    - ClientHelpRequest: The newly created help request entry.

    Raises:
    - HTTPException: If there is an issue while saving the request to the database.
    """
    request = ClientHelpRequest(
        date_posted=datetime.now(),
        owner_customer_no=current_user.customer_no,
        id=uuid4(),
        **new_request.dict()
    )
    try:
        db.add(request)
        db.commit()
        db.refresh(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, 
            detail="Failed to process the help request"
        ) from e
    return request


@router.post(
    "/report_problem",
    status_code=status.HTTP_201_CREATED,
    response_model=help_desk.ReportResponse,
    summary="Report an Issue",
    description=(
        "This endpoint allows authenticated users to report issues they are facing. "
        "The user can describe the problem, and the system will save the report for review "
        "by the relevant support team. Reports can include details provided in the request body."
    ),
    responses={
        201: {"description": "Problem report created successfully."},
        401: {"description": "Unauthorized. Access token is missing or invalid."},
        501: {"description": "Internal server error. Unable to save the problem report."},
    },
)
def report_problem(
    new_request: help_desk.Report, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(oauth.get_current_user)
):
    """
    Handles reporting problems or issues.

    Parameters:
    - new_request (schemas.Report): Data submitted by the user for reporting a problem.
    - db (Session): Database session dependency.
    - current_user (str): Current authenticated user obtained from the oauth dependency.

    Returns:
    - ClientReports: The newly created problem report entry.

    Raises:
    - HTTPException: If there is an issue while saving the report to the database.
    """
    request = ClientReports(
        date_posted=datetime.now(),
        owner_customer_no=current_user.customer_no,
        id=uuid4(),
        **new_request.dict()
    )
    try:
        db.add(request)
        db.commit()
        db.refresh(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, 
            detail="Failed to process the problem report"
        ) from e
    return request
