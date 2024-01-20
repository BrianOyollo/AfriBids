from fastapi import APIRouter, Response, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import schemas, models, utils




router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.get("/", response_model=List[schemas.UserOut], status_code=status.HTTP_200_OK)
async def get_all_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{user_id}", response_model=schemas.UserOut, status_code=status.HTTP_200_OK)
async def get_user(user_id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not exist!")
    
    return user

@router.post("/new", status_code=status.HTTP_201_CREATED)
async def register_user(new_user:schemas.UserRegistration, db:Session=Depends(get_db)):
    user = models.User(**new_user.model_dump())
    user.username = utils.generate_unique_username(db, user.display_name)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with that email already exists. Please try a different one")
    

@router.get("/{user_id}/profile", response_model=schemas.UserProfileOut, status_code=status.HTTP_200_OK)
async def get_user_profile(user_id:int, db:Session=Depends(get_db)):
    user_profile = db.query(models.User).filter(models.User.user_id==user_id).first()

    if user_profile == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Profile does not exist!')
    
    return user_profile
        

@router.put("/{user_id}/profile/update", response_model=schemas.UserProfileOut, status_code=status.HTTP_200_OK)
async def update_user_profile(user_id:int, profile_update:schemas.UpdateUserProfile, db:Session=Depends(get_db)):
    user_profile_query = db.query(models.User).filter(models.User.user_id==user_id)
    user_profile = user_profile_query.first()

    if user_profile == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exist!')
    
    # check if the current user is the profile's owner
    # check if email exists
    try:
        user_profile_query.update(profile_update.model_dump(exclude_unset=True), synchronize_session=False)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{profile_update.email} is already in use. Please try a different email!")
        
    return user_profile_query.first()

@router.delete("/{user_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(user_id:int, db:Session=Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.user_id == user_id)
    user_account = user_query.first()

    if user_account == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')
    
    # check if current user == account's owner

    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
