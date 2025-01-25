"""
JWT Authentication and Authorization Module.

This module provides functionality for generating and verifying JWT tokens, 
authenticating users, and validating HMAC signatures. It integrates with FastAPI's 
OAuth2PasswordBearer dependency for securing API endpoints.

Key Features:
-------------
1. **JWT Token Generation and Validation**:
   - Generate tokens with expiration timestamps for secure authentication.
   - Decode and validate tokens to retrieve user data.

2. **OAuth2 Integration**:
   - Supports OAuth2 bearer token scheme using FastAPI's OAuth2PasswordBearer.

3. **HMAC Signature Verification**:
   - Verifies the authenticity of payloads using HMAC with SHA-256.

Global Variables:
-----------------
- `oauth_scheme`: FastAPI OAuth2PasswordBearer dependency tied to the `login` endpoint.
- `SECRET_KEY`: Secret key used for signing JWTs and HMAC.
- `ALGORITHM`: Algorithm used for JWT encoding and decoding.
- `EXPIRATION`: Access token expiration time in minutes.

Dependencies:
-------------
- `fastapi`: For HTTP exception handling and security.
- `jose`: For encoding and decoding JWT tokens.
- `hmac` and `hashlib`: For HMAC signature verification.
- `base64`: For encoding HMAC signatures.

Notes:
------
- Ensure that `settings.secret_key` and `settings.algorithm` are securely configured 
  and loaded from environment variables or a configuration file.
"""

from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schema import users
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings
import hmac
import hashlib
import base64
import json

# OAuth2PasswordBearer dependency for retrieving bearer tokens
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")  # Ties an endpoint to function get_current_user

# Constants for JWT and HMAC
SECRET_KEY = settings.secret_key  # Secret key used for JWT signing and HMAC
ALGORITHM = settings.algorithm  # Algorithm used for JWT encoding/decoding
EXPIRATION = settings.access_token_expiration  # Access token expiration time in minutes


def create_token(data: dict) -> str:
    """
    Creates a JWT token with the provided data and expiration timestamp.

    Args:
        data (dict): A dictionary containing user or session-specific data 
                     to encode in the JWT payload.

    Returns:
        str: Encoded JWT token as a string.
    
    Example:
        >>> create_token({"customer_no": 12345})
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verify_token(token: str, credentials_exceptions: HTTPException):
    """
    Verifies the validity of a JWT token.

    Args:
        token (str): The JWT token to verify.
        credentials_exceptions (HTTPException): Exception to raise if token is invalid.

    Returns:
        schemas.TokenData: Decoded token data containing `customer_no`.

    Raises:
        HTTPException: If the token is invalid or does not contain the required fields.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        customer_no: int = payload.get("customer_no")
        if customer_no is None:
            raise credentials_exceptions
        data = users.TokenData(customer_no=customer_no)
    except JWTError:
        raise credentials_exceptions

    return data


def get_current_user(token: str = Depends(oauth_scheme)):
    """
    Retrieves the currently authenticated user from the JWT token.

    Args:
        token (str): Bearer token passed with the request.

    Returns:
        schemas.TokenData: Decoded token data containing user information.

    Raises:
        HTTPException: If the token is invalid or missing.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to Validate Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)


def verify_signature(payload: dict, signature: str) -> bool:
    """
    Verifies the HMAC signature of a payload to ensure data integrity.

    Args:
        payload (dict): The payload to verify.
        signature (str): The HMAC signature to compare.

    Returns:
        bool: `True` if the signature matches, `False` otherwise.

    Example:
        >>> payload = {"key": "value"}
        >>> signature = "generated_signature_string"
        >>> verify_signature(payload, signature)
        True
    """
    # Convert payload to string
    payload_string = json.dumps(payload, separators=(",", ":"))

    # Calculate HMAC using SHA-256
    computed_hmac = hmac.new(SECRET_KEY.encode(), payload_string.encode(), hashlib.sha256)
    computed_signature = base64.b64encode(computed_hmac.digest()).decode()

    return computed_signature == signature
