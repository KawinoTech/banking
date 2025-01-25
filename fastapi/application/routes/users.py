"""
This module provides a set of FastAPI endpoints for managing user-related operations. 
It includes routes for creating users, retrieving customer information, and logging in. 
The module interacts with a database to persist user data and provides API responses in the appropriate 
formats using Pydantic models defined in the schemas module.
"""
from fastapi import Depends, status, APIRouter, HTTPException
from .. import oauth
from ..models.users import Customer
from ..schema import users
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta, datetime
from ..config import settings

# Initialize the router for the "/post" prefix
router = APIRouter(
    prefix="/post",
    tags=["User Management"],  # Assign this router to a specific documentation category
)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=users.ResponseUser)
def create_user(user: users.User, db: Session = Depends(get_db)):
    """
    Creates a new user by adding their details to the database.

    Args:
        user (schemas.User): User data to create a new customer, validated via Pydantic schema.
        db (Session): The database session used to interact with the database.

    Returns:
        ResponseUser: The created user's data as a response.

    HTTP Status Codes:
        - 201 Created: Successful creation of a new user.
    """
    new_user = Customer(**user.dict())  # Create a Customer object from the user data
    db.add(new_user)  # Add new customer to the session
    db.commit()  # Commit the changes to the database
    db.refresh(new_user)  # Refresh to get updated customer data after commit
    return new_user  # Return the created user data


@router.get("/get_customers", status_code=status.HTTP_200_OK, response_model=List[users.ResponseUser])
def get_users(db: Session = Depends(get_db)):
    """
    Retrieves all users (customers) from the database.

    Args:
        db (Session): The database session used to query the database.

    Returns:
        List[ResponseUser]: A list of customer objects.

    HTTP Status Codes:
        - 200 OK: The list of customers is successfully retrieved.
    """
    users = db.query(Customer).all()  # Retrieve all customers from the database
    return users  # Return the list of users


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user_credentials: users.LoginUser, db: Session = Depends(get_db)):
    """
    Logs in a customer by validating the credentials (customer number and password) and generating an access token.

    Args:
        user_credentials (schemas.LoginUser): Customer's credentials, validated via Pydantic schema.
        db (Session): The database session used to query the database.

    Returns:
        dict: A dictionary with the access token, expiration time, and customer number.

    Raises:
        HTTPException: If the credentials are invalid (user not found or incorrect password).

    HTTP Status Codes:
        - 200 OK: Successful login with access token returned.
    """
    # Look up the user by customer number
    user = db.query(Customer).filter(Customer.customer_no == user_credentials.customer_no).first()

    # If user is not found, raise 404 error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )

    # If password doesn't match, raise 403 error
    if not user.check_password(user_credentials.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # Generate the access token
    access_token = oauth.create_token(data={"customer_no": user.customer_no})

    # Set the expiration date for the access token
    expire = datetime.now() + timedelta(minutes=settings.access_token_expiration)

    # Return the access token and expiration time along with the customer number
    return {
        "access_token": access_token,
        "expires_in": expire.isoformat(),
        "customer_no": user.customer_no
    }

           