from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from dateutil import parser
from typing import Union, List


#  bids
class NewBid(BaseModel):
    amount:float
    
class BidResponse(BaseModel):
    bid_id:int
    bidder: Union[int, 'UserOut']
    auction_id:int
    created_at:datetime
    amount:float

# users   
class UserRegistration(BaseModel):
    email:EmailStr
    display_name:str
    password:str

class UserOut(BaseModel):
    model_config: ConfigDict(from_attributes=True) 

    user_id:int
    username:str
    display_name:str
    location:str|None=None
    created_at:datetime
    is_active:bool
    # bids:BidResponse

class UpdateUserProfile(BaseModel):
    display_name:str|None=None
    email:EmailStr|None=None
    phone:str|None=None
    location:str|None=None

class UserProfileOut(BaseModel):
    username:str
    display_name:str
    email:EmailStr
    phone:str|None=None
    created_at:datetime
    location:str|None=None

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
class NewAuction(BaseModel):
    item_name:str
    item_description:str
    item_category:int
    reserve_status:int
    reserve_price:float|None=None
    seller:int


class GeneralAuctionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    auction_id:int
    item_name:str
    item_description:str
    start_time:datetime
    end_time:datetime
    current_bid:float
    reserve_price:float
    bids: List[BidResponse]
    itemcategory:ItemCategoryResponse
    reservestatus:ReserveStatusResponse
    auctionstatus:AuctionStatusResponse
    user:UserOut

class CancelAuction(BaseModel):
    reason:str|None=None
