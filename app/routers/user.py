from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models, utils, database

router = APIRouter(prefix="/users" , tags=["Users"])

@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.ResponseUser)
def create_user(user: schemas.CreateUser, db: Session = Depends(database.get_db) ):
    new_user = models.Users(**user.model_dump())
    new_user.password = utils.hash_password(new_user.password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}" ,status_code=status.HTTP_200_OK , response_model=schemas.ResponseUser)
def get_user(id: int , db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"ID : {id} is not found")
    
    return user