from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth
from app.database import get_db

router = APIRouter()

@router.post("/requests/", response_model=schemas.Request)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_request = models.Request(user_id=current_user.id, **request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.get("/requests/", response_model=List[schemas.Request])
def read_requests(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.is_admin:
        return db.query(models.Request).filter(models.Request.user_id == current_user.id).all()
    return db.query(models.Request).all()

@router.put("/requests/{request_id}", response_model=schemas.Request)
def update_request(request_id: int, request: schemas.RequestBase, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    for key, value in request.dict().items():
        setattr(db_request, key, value)
    db.commit()
    db.refresh(db_request)
    return db_request