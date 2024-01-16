from fastapi import APIRouter, Response, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session,joinedload
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import schemas, models, utils
from typing import List



router = APIRouter(
    prefix='/auction_constants',
    tags=['Auction Statuses']
)

# reserve statuses
@router.post("/reserve_status/new", response_model=schemas.ReserveStatusResponse, status_code=status.HTTP_201_CREATED)
async def new_reserve_status(newstatus:schemas.NewReserveStatus, db:Session=Depends(get_db)):
    new_status = models.ReserveStatus(**newstatus.model_dump())

    try:
        db.add(new_status)
        db.commit()
        db.refresh(new_status)
        return new_status

    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error creating a new reserve status!")


@router.get("/reserve_status",response_model=List[schemas.ReserveStatusResponse], status_code=status.HTTP_200_OK)
async def get_reserve_statuses(db:Session=Depends(get_db)):
    reserve_statuses = db.query(models.ReserveStatus).all()
    return reserve_statuses

@router.get("/reserve_status/{status_id}", response_model=schemas.ReserveStatusResponse, status_code=status.HTTP_200_OK)
async def get_reserve_status(status_id:int, db:Session=Depends(get_db)):
    reserve_status = db.query(models.ReserveStatus).filter(models.ReserveStatus.status_id == status_id).first()

    if reserve_status == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserve status not found!")
    
    return reserve_status

@router.put("/reserve_status/{status_id}/update", response_model=schemas.ReserveStatusResponse, status_code=status.HTTP_200_OK)
async def update_reserve_status(status_id:int, status_update:schemas.UpdateReserveStatus, db:Session=Depends(get_db)):
    reserve_status = db.query(models.ReserveStatus).filter(models.ReserveStatus.status_id==status_id)

    if reserve_status.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Reserve status not found!')
    
    try:
        reserve_status.update(status_update.model_dump(exclude_unset=True), synchronize_session=False)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Update failed. Please try again')
    
    return reserve_status.first()

@router.delete("/reserve_status/{status_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reserve_status(status_id:int, db:Session=Depends(get_db)):
    reserve_status = db.query(models.ReserveStatus).filter(models.ReserveStatus.status_id==status_id)

    if reserve_status.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Reserve status not found!')
    
    try:
        reserve_status.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Error encountered when deleting status. Please try again')

# auction_status
@router.post("/auction_status/new", response_model=schemas.AuctionStatusResponse, status_code=status.HTTP_201_CREATED)
async def new_auction_status(newstatus:schemas.NewAuctionStatus, db:Session=Depends(get_db)):
    new_status = models.AuctionStatus(**newstatus.model_dump())

    try:
        db.add(new_status)
        db.commit()
        db.refresh(new_status)
        return new_status

    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error creating a new auction status!")


@router.get("/auction_status",response_model=List[schemas.AuctionStatusResponse], status_code=status.HTTP_200_OK)
async def get_auction_statuses(db:Session=Depends(get_db)):
    auction_statuses = db.query(models.AuctionStatus).all()
    return auction_statuses

@router.get("/auction_status/{status_id}", response_model=schemas.AuctionStatusResponse, status_code=status.HTTP_200_OK)
async def get_reserve_status(status_id:int, db:Session=Depends(get_db)):
    auction_status = db.query(models.AuctionStatus).filter(models.AuctionStatus.status_id == status_id).first()

    if auction_status == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction status not found!")
    
    return auction_status

@router.put("/auction_status/{status_id}/update", response_model=schemas.AuctionStatusResponse, status_code=status.HTTP_200_OK)
async def update_reserve_status(status_id:int, status_update:schemas.UpdateAuctionStatus, db:Session=Depends(get_db)):
    auction_status = db.query(models.AuctionStatus).filter(models.AuctionStatus.status_id==status_id)

    if auction_status.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Auction status not found!')
    
    try:
        auction_status.update(status_update.model_dump(exclude_unset=True), synchronize_session=False)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Update failed. Please try again')
    
    return auction_status.first()

@router.delete("/auction_status/{status_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reserve_status(status_id:int, db:Session=Depends(get_db)):
    auction_status = db.query(models.AuctionStatus).filter(models.AuctionStatus.status_id==status_id)

    if auction_status.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Auction status not found!')
    
    try:
        auction_status.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Error encountered when deleting status. Please try again')
    

# item_categories
@router.post("/item_category/new", response_model=schemas.ItemCategoryResponse, status_code=status.HTTP_201_CREATED)
async def new_item_category(newcategory:schemas.NewItemCategory, db:Session=Depends(get_db)):
    new_category = models.ItemCategory(**newcategory.model_dump())

    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error creating a new item category!")


@router.get("/item_category",response_model=List[schemas.ItemCategoryResponse], status_code=status.HTTP_200_OK)
async def get_item_categories(db:Session=Depends(get_db)):
    item_categories = db.query(models.ItemCategory).all()
    return item_categories

@router.get("/item_category/{category_id}", response_model=schemas.ItemCategoryResponse, status_code=status.HTTP_200_OK)
async def get_item_category(category_id:int, db:Session=Depends(get_db)):
    item_category= db.query(models.ItemCategory).filter(models.ItemCategory.category_id == category_id).first()

    if item_category == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category status not found!")
    
    return item_category

@router.put("/item_category/{category_id}/update", response_model=schemas.ItemCategoryResponse, status_code=status.HTTP_200_OK)
async def update_item_category(category_id:int, category_update:schemas.UpdateItemCategory, db:Session=Depends(get_db)):
    item_category = db.query(models.ItemCategory).filter(models.ItemCategory.category_id==category_id)

    if item_category.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item category not found!')
    
    try:
        item_category.update(category_update.model_dump(exclude_unset=True), synchronize_session=False)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Update failed. Please try again')
    
    return item_category.first()

@router.delete("/item_category/{category_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reserve_status(category_id:int, db:Session=Depends(get_db)):
    item_category = db.query(models.ItemCategory).filter(models.ItemCategory.category_id==category_id)

    if item_category.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item category not found!')
    
    try:
        item_category.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Error encountered when deleting category. Please try again')