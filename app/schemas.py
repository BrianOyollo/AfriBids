from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import datetime
from dateutil import parser


class UserRegistration(BaseModel):
    email:EmailStr
    display_name:str
    password:str

class UserOut(BaseModel):
    user_id:int
    username:str
    display_name:str
    location:str|None=None
    created_at:datetime

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