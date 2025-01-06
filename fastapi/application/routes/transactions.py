from fastapi import  Depends, status, APIRouter, HTTPException, status
import logging
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.exc import IntegrityError
from .. import models, schemas, oauth
from ..database import  get_db
from sqlalchemy.orm import Session
from uuid import uuid4
DAILY_LIMIT = 100
router = APIRouter(prefix="/post")
logger = logging.getLogger(__name__)

@router.post("/transfer", status_code=status.HTTP_201_CREATED,
             response_model=schemas.ResponseTransact,
             dependencies=[Depends(RateLimiter(times=10, seconds=60))],
             tags=["transactions"],
             summary="Transfer funds between accounts",
             description="This endpoint allows users to transfer funds between from bank accounts to mobile(MPESA, AIRTEL, Telcom) adhering to specified limits.")
def transfer(transaction: schemas.Transaction,
             db: Session = Depends(get_db),
             current_user: str = Depends(oauth.get_current_user)):
    new_transaction = models.Transfer(id = uuid4(), ref_no = uuid4(), **transaction.payload)
    account = db.query(models.Account).filter(models.Account.account_no == transaction.payload['account']).first()
    try:
        '''
        This feature will be soon updated
        if not oauth.verify_signature(transaction.payload, transaction.signature):
            raise HTTPException(status_code=400, detail="Invalid signature")'''
        if not account:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account does not exist."
        )
        if transaction.payload['amount'] <= 0:
            raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Transaction amount must be greater than zero."
        )
        if account.account_balance < transaction.payload['amount']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed. Insufficient Funds")
        account.account_balance -= transaction.payload['amount']
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        logger.info(f"User {current_user} transferred {transaction.payload['amount']} to account {transaction.payload['amount']}")
        return new_transaction
    except IntegrityError as e:
        db.rollback()  # Important for consistency
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
    )


@router.post("/buygoods",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.ResponseTransact,
             tags=["transactions"],
             summary="",
             description="",
             dependencies=[Depends(RateLimiter(times=10, seconds=60))]
             )
def buygoods(transaction: schemas.Transaction, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    new_transaction = models.BuyGoods(id = uuid4(), ref_no = uuid4(), **transaction.payload)
    account = db.query(models.Account).filter(models.Account.account_no == transaction.payload['account']).first()
    try:
        if not account:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account does not exist."
        )
        if transaction.payload['amount'] <= 0:
            raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Transaction amount must be greater than zero."
        )
        if account.account_balance < transaction.payload['amount']:
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed. Insufficient Funds")
        account.account_balance -= transaction.payload['amount']
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        logger.info(f"User {current_user} transferred {transaction.payload['amount']} to account {transaction.payload['amount']}")
        return new_transaction
    except IntegrityError as e:
        db.rollback()  # Important for consistency
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
    )


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