from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from dateutil import parser


class UserRegistration(BaseModel):
    email:EmailStr
    username:str
    password:str

class UserOut(BaseModel):
    user_id:int
    username:str
    location:str
    created_at:datetime

class UpdateUserProfile(BaseModel):
    username:str|None=None
