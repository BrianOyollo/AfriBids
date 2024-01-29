from pydantic import BaseModel, EmailStr, ConfigDict
from dataclasses import dataclass
from fastapi import Form
from datetime import datetime
from dateutil import parser
from typing import Optional, Union, List


#  for bids
class NewBid(BaseModel):
    amount:float

class BidderInfo(BaseModel):
    user_id:int
    username:str
    display_name:str
    location:str|None=None
    created_at:datetime
    is_active:bool

class FullBidProfile(BaseModel):
    bid_id:int
    amount:float
    created_at:datetime
    bidder:BidderInfo

# item categories
class ItemCategoryResponse(BaseModel):
    category_id:int
    category_name:str

class NewItemCategory(BaseModel):
    category_name:str

class UpdateItemCategory(BaseModel):
    category_name:str|None=None


# auction status
class AuctionStatusResponse(BaseModel):
    status_id:int
    status:str
    status_description:str

class NewAuctionStatus(BaseModel):
    status:str
    status_description:str

class UpdateAuctionStatus(BaseModel):
    status:str|None=None
    status_description:str|None=None


# reserve status
class NewReserveStatus(BaseModel):
    status:str
    status_description:str

class UpdateReserveStatus(BaseModel):
    status:str|None=None
    status_description:str|None=None

class ReserveStatusResponse(BaseModel):
    status_id:int
    status:str
    status_description:str

# auctions
# class NewAuction(BaseModel):
#     item_name:str
#     item_description:str
#     item_category:int
#     reserve_status:int
#     reserve_price:float|None=None
#     seller:int
    
@dataclass
class NewAuction:
    item_name:str = Form(...)
    item_description:str = Form(...)
    item_category:int = Form(...)
    reserve_status:int = Form(...)
    reserve_price: float= Form(None)
    seller:int = Form(...)


class AuctionImages(BaseModel):
    image_description: str|None=None
    image_url:str

class FullAuctionProfile(BaseModel):
    auction_id:int
    item_name:str
    item_description:str
    start_time:datetime
    end_time:datetime
    current_bid:float
    itemcategory:ItemCategoryResponse
    reservestatus:ReserveStatusResponse
    auctionstatus:AuctionStatusResponse
    images:List[AuctionImages]
    bids: List[FullBidProfile]
    user:BidderInfo # bidders

class CancelAuction(BaseModel):
    reason:str|None=None






# for user
class UserAuctionData(BaseModel):
    auction_id:int
    item_name:str
    item_description:str
    end_time:datetime
    current_bid:float
    itemcategory:ItemCategoryResponse
    reservestatus:ReserveStatusResponse
    auctionstatus:AuctionStatusResponse

class UserBidData(BaseModel):
    bid_id:int
    auction:UserAuctionData
    created_at:datetime
    amount:float

class FullUserProfileUnAuthorized(BaseModel):
    model_config: ConfigDict(from_attributes=True) 

    user_id:int
    username:str
    display_name:str
    location:str|None=None
    created_at:datetime
    is_active:bool
    bids:List[UserBidData]
    auctions:List[UserAuctionData]


class FullUserProfileAuthorized(BaseModel):
    user_id:int
    username:str
    display_name:str
    email:EmailStr
    phone:str|None=None
    is_active:bool
    created_at:datetime
    location:str|None=None
    bids:List[UserBidData]
    auctions:List[UserAuctionData]

class UpdateUserProfile(BaseModel):
    display_name:str|None=None
    email:EmailStr|None=None
    phone:str|None=None
    location:str|None=None

class UserRegistration(BaseModel):
    email:EmailStr
    display_name:str
    password:str