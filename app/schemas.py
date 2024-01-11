from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserIn(BaseModel):
    email:EmailStr
    username:str
    password:str

class UserOut(BaseModel):
    user_id:int
    username:str
    location:str
    created_at:datetime
