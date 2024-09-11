from fastapi import  Depends, status, APIRouter, HTTPException
from .. import models, schemas, oauth
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/post")
@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/get_users", status_code=status.HTTP_200_OK, response_model=List[schemas.ResponseUser])
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user_credentials: schemas.LoginUser, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.customer_no == user_credentials.customer_no).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    if not user.check_password(user_credentials.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    
    access_token = oauth.create_token(data = {"customer_no": user.customer_no})
    
    return {"access_token": access_token,
            "customer_no": user.customer_no}
           