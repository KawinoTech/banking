from fastapi import  Depends, status, APIRouter, HTTPException, status
from .. import models, schemas, oauth
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4
router = APIRouter(prefix="/post")

'''
@router.get("/{id}", status_code=status.HTTP_200_OK)
#id - path parameter always a string
#parameter id is converted to int
def get_idea(id: int, db: Session = Depends(get_db)):
    idea = db.query(models.Idea).filter(models.Idea.id == id).first()
    return idea

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ResponseIdea])
def get_ideas(db: Session = Depends(get_db),
              current_user : str = Depends(oauth.get_current_user),
              limit: int = 10,
              skip: int = 10,
              search: Optional[str] = ""):
    ideas = db.query(models.Idea).filter(models.Idea.title.contains(search)).limit(limit).offset(skip).all()
    return ideas
'''

@router.post("/open_new_account", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseAccount)
#Post automatically saves users post in the form of pydantic model
#It is then stored in new_post. Every pydantic model has a .dict(converts to a python dict)
def create_account(new_account: schemas.Account, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    account = models.Account(owner_customer_no = current_user.customer_no, account_no = uuid4(), **new_account.dict())
    try:
        db.add(account)
        db.commit()
        db.refresh(account)

    except:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed")
    return account

@router.get("/get_user_accounts", status_code=status.HTTP_200_OK, response_model=List[schemas.ResponseAccount1])
def get_user_accounts(db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    accounts = db.query(models.Account).filter(models.Account.owner_customer_no == current_user.customer_no).all()
    return accounts

