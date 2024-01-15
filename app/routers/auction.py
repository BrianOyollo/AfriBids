from fastapi import APIRouter, Response, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import schemas, models, utils



router = APIRouter(
    prefix='/auctions',
    tags=['Auctions']
)


@router.get("/")
async def all_auctions():
    return {'message':'All auctions!'}
