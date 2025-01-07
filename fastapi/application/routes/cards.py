from fastapi import  Depends, status, APIRouter, HTTPException, status
from .. import models, schemas, oauth
from datetime import datetime
from ..database import  get_db
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List
from dateutil.relativedelta import relativedelta
router = APIRouter(prefix="/post")

@router.post("/debit_card_application", status_code=status.HTTP_201_CREATED, response_model=schemas.CardApplicationResponse)
def apply_debit_card(new_card: schemas.CardApplication, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    request = models.DebitCards(card_no = models.BaseCards.generate_card_no(),
                                date_issued = datetime.now(),
                                expiry_date = datetime.now() + relativedelta(years=3),
                                       date_requested = datetime.now(),
                                       owner_customer_no = current_user.customer_no,
                                       id = uuid4(), **new_card.payload)
    try:
        db.add(request)
        db.commit()
        db.refresh(request)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed")
    return request

@router.get("/get_user_debit_cards", status_code=status.HTTP_200_OK, response_model=List[schemas.GetDebitCards])
def get_user_accounts(db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    accounts = (
    db.query(models.DebitCards).filter(
        models.Account.owner_customer_no == current_user.customer_no).all())
    for account in accounts:
        account.reformat_card_no()
        account.truncate_uuid()
        account.truncate_datetime()
        print(account.date_issued)
    return accounts