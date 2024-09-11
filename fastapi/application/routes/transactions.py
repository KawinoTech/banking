from fastapi import  Depends, status, APIRouter, HTTPException, status
from .. import models, schemas, oauth
from ..database import  get_db
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List, Optional
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
@router.post("/transfer", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseTransfer)
#Post automatically saves users post in the form of pydantic model
#It is then stored in new_post. Every pydantic model has a .dict(converts to a python dict)
def transfer(transaction: schemas.Transfer, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    new_transaction = models.Transfer(id = uuid4(), ref_no = uuid4(), **transaction.dict())
    account = db.query(models.Account).filter(models.Account.account_no == transaction.account).first()
    try:
        if account.account_balance < transaction.amount:
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed. Insufficient Funds")
        account.account_balance -= transaction.amount
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
    except:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed")
    return new_transaction


@router.post("/buygoods", status_code=status.HTTP_201_CREATED, response_model=schemas.BuyGoods)
#Post automatically saves users post in the form of pydantic model
#It is then stored in new_post. Every pydantic model has a .dict(converts to a python dict)
def buygoods(transaction: schemas.BuyGoods, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    new_transaction = models.BuyGoods(id = uuid4(), ref_no = uuid4(), **transaction.dict())
    account = db.query(models.Account).filter(models.Account.account_no == transaction.account).first()
    try:
        if account.account_balance < transaction.amount:
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed. Insufficient Funds")
        account.account_balance -= transaction.amount
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
    except:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed")
    return new_transaction


@router.post("/paybill", status_code=status.HTTP_201_CREATED, response_model=schemas.PayBill)
#Post automatically saves users post in the form of pydantic model
#It is then stored in new_post. Every pydantic model has a .dict(converts to a python dict)
def paybill(transaction: schemas.PayBill, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    new_transaction = models.PayBill(id = uuid4(), ref_no = uuid4(), **transaction.dict())
    account = db.query(models.Account).filter(models.Account.account_no == transaction.account).first()
    try:
        if account.account_balance < transaction.amount:
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed. Insufficient Funds")
        account.account_balance -= transaction.amount
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
    except:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed")
    return new_transaction
'''
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_idea(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    idea = db.query(models.Idea).filter(models.Idea.id == id).first()
    if idea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    if idea.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    idea.delete(synchroize_session = False)
    db.commit()
'''