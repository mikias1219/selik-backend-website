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
    db_tutorial = models.Tutorial(
        title=tutorial.title,
        content=tutorial.content,
        tutorial_type=tutorial.tutorial_type,
        price=tutorial.price,
        posted_date=tutorial.posted_date,
        video_url=tutorial.video_url,
        video_file=tutorial.video_file
    )
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
    db_tutorial.title = tutorial.title
    db_tutorial.content = tutorial.content
    db_tutorial.tutorial_type = tutorial.tutorial_type
    db_tutorial.price = tutorial.price
    db_tutorial.posted_date = tutorial.posted_date
    db_tutorial.video_url = tutorial.video_url
    db_tutorial.video_file = tutorial.video_file
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