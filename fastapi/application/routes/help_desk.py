from fastapi import  Depends, status, APIRouter, HTTPException, status
from .. import models, schemas, oauth
from datetime import datetime
from ..database import  get_db
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List, Optional
router = APIRouter(prefix="/post")

@router.post("/request_help", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseHelp)
def request_help(new_request: schemas.HelpDesk, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    request = models.ClientHelpRequest(date_posted = datetime.now(), owner_customer_no = current_user.customer_no, id = uuid4(), **new_request.dict())
    try:
        db.add(request)
        db.commit()
        db.refresh(request)

    except:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed")
    return request
@router.post("/report_problem", status_code=status.HTTP_201_CREATED, response_model=schemas.ReportResponse)
def report_problem(new_request: schemas.Report, db: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    request = models.ClientReports(date_posted = datetime.now(), owner_customer_no = current_user.customer_no, id = uuid4(), **new_request.dict())
    try:
        print(request)
        db.add(request)
        db.commit()
        db.refresh(request)

    except:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Failed")
    return request