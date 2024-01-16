from fastapi import APIRouter, Response, status, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session,joinedload
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import schemas, models, utils
from typing import List



router = APIRouter(
    prefix='/auctions',
    tags=['Auctions']
)


@router.get("/",response_model=List[schemas.GeneralAuctionResponse],status_code=status.HTTP_200_OK)
async def all_auctions(db:Session=Depends(get_db), q:str|None=None):
    auctions = (
        db.query(models.Auction)
        .join(models.User, models.Auction.seller == models.User.user_id, isouter=True)
        .join(models.ItemCategory, models.Auction.item_category == models.ItemCategory.category_id, isouter=True)
        .join(models.ReserveStatus, models.Auction.reserve_status == models.ReserveStatus.status_id, isouter=True)
        .join(models.AuctionStatus, models.Auction.auction_status == models.AuctionStatus.status_id, isouter=True)
        ).all()
    return auctions

@router.get("/{auction_id}", response_model=schemas.GeneralAuctionResponse, status_code=status.HTTP_200_OK)
async def get_auction(auction_id:int, db:Session=Depends(get_db)):
    auction = (
        db.query(models.Auction)
        .join(models.User, models.Auction.seller == models.User.user_id, isouter=True)
        .join(models.ItemCategory, models.Auction.item_category == models.ItemCategory.category_id, isouter=True)
        .join(models.ReserveStatus, models.Auction.reserve_status == models.ReserveStatus.status_id, isouter=True)
        .join(models.AuctionStatus, models.Auction.auction_status == models.AuctionStatus.status_id, isouter=True)
        ).options(
            joinedload(models.Auction.itemcategory),
            joinedload(models.Auction.reservestatus),
            joinedload(models.Auction.auctionstatus),
            joinedload(models.Auction.user),

        ).filter(models.Auction.auction_id == auction_id).first()
    
    if auction == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction does not exists!")
    
    return auction

@router.post("/new", response_model=schemas.GeneralAuctionResponse,status_code=status.HTTP_201_CREATED)
async def new_auction(auction:schemas.NewAuction, db:Session=Depends(get_db)):
    new_auction = models.Auction(**auction.model_dump())

    try:
        db.add(new_auction)
        db.commit()
        db.refresh(new_auction)
        return new_auction
    
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error creating an auction!')

    
@router.put("/{auction_id}/cancel", status_code=status.HTTP_200_OK)
async def cancel_auction(auction_id:int,cancel_auction:schemas.CancelAuction, db:Session=Depends(get_db)):
    auction = db.query(models.Auction).filter(models.Auction.auction_id == auction_id).first()

    if auction == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction not found!")
    
    if auction.auction_status != 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only ongoing auctions can be cancelled")
    
    try:
        auction.auction_status = 3 # or status_id for 'cancelled'
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error countered while cancelling the auction. Please try again")

    cancelled_auction = db.query(models.Auction).filter(models.Auction.auction_id == auction_id).first()
    return cancelled_auction, cancel_auction
