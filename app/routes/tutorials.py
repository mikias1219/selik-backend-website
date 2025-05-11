from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth
from app.database import get_db

router = APIRouter()

@router.post("/tutorials/", response_model=schemas.Tutorial)
def create_tutorial(tutorial: schemas.TutorialCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_tutorial = models.Tutorial(**tutorial.dict())
    db.add(db_tutorial)
    db.commit()
    db.refresh(db_tutorial)
    return db_tutorial

@router.get("/tutorials/", response_model=List[schemas.Tutorial])
def read_tutorials(db: Session = Depends(get_db)):
    return db.query(models.Tutorial).all()

@router.put("/tutorials/{tutorial_id}", response_model=schemas.Tutorial)
def update_tutorial(tutorial_id: int, tutorial: schemas.TutorialCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_tutorial = db.query(models.Tutorial).filter(models.Tutorial.id == tutorial_id).first()
    if not db_tutorial:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    for key, value in tutorial.dict().items():
        setattr(db_tutorial, key, value)
    db.commit()
    db.refresh(db_tutorial)
    return db_tutorial

@router.delete("/tutorials/{tutorial_id}")
def delete_tutorial(tutorial_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_tutorial = db.query(models.Tutorial).filter(models.Tutorial.id == tutorial_id).first()
    if not db_tutorial:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    db.delete(db_tutorial)
    db.commit()
    return {"detail": "Tutorial deleted"}