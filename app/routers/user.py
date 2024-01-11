from fastapi import APIRouter, Response, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models




router = APIRouter(
    prefix='/users',
    tags=['users']
)



@router.get("/", response_model=List[schemas.UserOut], status_code=status.HTTP_200_OK)
async def get_all_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{user_id}", response_model=schemas.UserOut)
async def get_user(user_id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exist!")
    
    return user

@router.post("/new", status_code=status.HTTP_201_CREATED)
async def register_user(new_user:schemas.UserRegistration, db:Session=Depends(get_db)):
    user = models.User(**new_user.model_dump())
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"User with that email or phone number already exists. Please try a different one"})