from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import  Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings
import hmac
import hashlib
import base64
import json

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login') #Ties an endpoint to function get_current user
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION = settings.access_token_expiration

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

def verify_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        customer_no :int = payload.get("customer_no")
        if customer_no is None:
            raise credentials_exceptions
        data = schemas.TokenData(customer_no = customer_no)
    except JWTError:
        raise credentials_exceptions
    
    return data
def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Unable to Validate Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_token(token, credentials_exception)

def verify_signature(payload: dict, signature: str) -> bool:
    # Convert payload to string
    payload_string = json.dumps(payload, separators=(',', ':'))

    # Calculate HMAC using the same hashing method (SHA256) as in the frontend
    computed_hmac = hmac.new(SECRET_KEY, payload_string.encode(), hashlib.sha256)
    computed_signature = base64.b64encode(computed_hmac.digest()).decode()

    return computed_signature == signature