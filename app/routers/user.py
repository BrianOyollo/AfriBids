from fastapi import APIRouter, Response, status, Depends
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