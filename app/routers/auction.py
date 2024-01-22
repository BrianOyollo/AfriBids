from fastapi import APIRouter, Response, status, Depends, HTTPException, UploadFile, File
from typing import List
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import schemas, models, utils
from typing import List
from datetime import datetime
import os 
import pytz
from dotenv import load_dotenv

load_dotenv()
BID_JUMP = os.getenv('BID_JUMP')

router = APIRouter(
    prefix='/auctions',
    tags=['Auctions']
)


@router.get("/",response_model=List[schemas.FullAuctionProfile],status_code=status.HTTP_200_OK)
async def all_auctions(db:Session=Depends(get_db), q:str|None=None):
    auctions = (
        db.query(models.Auction)
        .join(models.User, models.Auction.seller == models.User.user_id, isouter=True)
        .join(models.ItemCategory, models.Auction.item_category == models.ItemCategory.category_id, isouter=True)
        .join(models.ReserveStatus, models.Auction.reserve_status == models.ReserveStatus.status_id, isouter=True)
        .join(models.AuctionStatus, models.Auction.auction_status == models.AuctionStatus.status_id, isouter=True)
        .join(models.Bid, models.Auction.auction_id == models.Bid.auction_id, isouter=True)
        ).all()
    return auctions

@router.get("/{auction_id}", response_model=schemas.FullAuctionProfile, status_code=status.HTTP_200_OK)
async def get_auction(auction_id:int, db:Session=Depends(get_db)):
    auction = (
        db.query(models.Auction)
        .join(models.User, models.Auction.seller == models.User.user_id, isouter=True)
        .join(models.ItemCategory, models.Auction.item_category == models.ItemCategory.category_id, isouter=True)
        .join(models.ReserveStatus, models.Auction.reserve_status == models.ReserveStatus.status_id, isouter=True)
        .join(models.AuctionStatus, models.Auction.auction_status == models.AuctionStatus.status_id, isouter=True)
        .join(models.Bid, models.Auction.auction_id == models.Bid.auction_id, isouter=True)
        ).options(
            joinedload(models.Auction.itemcategory),
            joinedload(models.Auction.reservestatus),
            joinedload(models.Auction.auctionstatus),
            joinedload(models.Auction.user),
            joinedload(models.Auction.bids)

        ).filter(models.Auction.auction_id == auction_id).first()
    
    if auction == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction does not exists!")
    
    return auction

@router.post("/new", response_model=schemas.FullAuctionProfile,status_code=status.HTTP_201_CREATED)
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


@router.post("/{auction_id}/bid", status_code=status.HTTP_201_CREATED)
async def place_bid(auction_id:int, new_bid:schemas.NewBid, db:Session=Depends(get_db)):
    auction = db.query(models.Auction).filter(models.Auction.auction_id == auction_id).with_for_update().first()
    # check if the current user != seller

    # check if the auction is ongoing; other statuses don't allow bids
    if auction.auction_status != 1: # id of 'ongoing'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can only place bids for ongoing options")

    # check if the bid is higher than the current highest bid
    if new_bid.amount <= auction.current_bid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"A new bid must be higher than the current highest bid! ({auction.current_bid})")
    
    # check if the bid_jump is met (min amount allowd)
    if (new_bid.amount - auction.current_bid) < float(BID_JUMP):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Your bid should atleast Ksh.{BID_JUMP} higher than the current bid({auction.current_bid})')
    
    #  if auction has a reserve price, bid > reserve price
    if auction.reserve_status == 1: # id of 'reserve'
        if new_bid.amount <= auction.reserve_price:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This auction has a reserve price. Please place a bid higher than it's reserve price({auction.reserve_price})")
    
    
    # check if the bid time is before auction end_time
    bid_time = datetime.now(pytz.utc)
    if bid_time > auction.end_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'This auction has ended and is no longer accepting bids.')
    
    bid = models.Bid(**new_bid.model_dump())
    bid.auction_id = auction_id
    bid.bidder_id = 1 # will get this from id of the current_user
    try:
        db.add(bid)
        auction.current_bid = new_bid.amount
        db.commit()
        db.refresh(bid)
        return {"Message:Bid placed successfully!"}
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error placing bid. Please try again")