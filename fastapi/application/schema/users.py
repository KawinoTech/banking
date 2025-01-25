from pydantic import BaseModel

class User(BaseModel):
    full_name: str
    pin : str
    password_hash : str 
    email : str
    customer_no: int

    class Config:
        from_attributes = True
class ResponseUser(BaseModel):
    full_name: str
    id : str



class LoginUser(BaseModel):
    customer_no: int
    password_hash: str
class TokenData(BaseModel):
    customer_no: int