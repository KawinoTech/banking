from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import  Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings

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