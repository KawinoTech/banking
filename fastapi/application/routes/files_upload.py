from fastapi import FastAPI, File, Form, UploadFile, Depends, APIRouter
from typing import List
from .. import schemas



router = APIRouter(prefix="/post")

@router.post("/upload", response_model=List[schemas.SignatoryResponse])
def upload_signatories(
    names: List[str] = Form(...),
    emails: List[str] = Form(...),
    files: List[UploadFile] = File(...),
):
    signatories = []
    for name, email, file in zip(names, emails, files):
        # Process or save files as needed
        file_location = f"uploads/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(file.read())

        signatories.append(
            schemas.SignatoryResponse(name=name, email=email, file_name=file.filename)
        )
    
    return signatories