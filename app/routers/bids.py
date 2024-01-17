from fastapi import APIRouter, Response, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session,joinedload
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import schemas, models, utils
from typing import List



router = APIRouter(
    prefix='/bids',
    tags=['Bids']
)

@router.get("/{bid_id}")
async def get_bids():
    pass