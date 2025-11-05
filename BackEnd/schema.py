from uuid import UUID
from click import Option
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Union
from datetime import date, datetime, time 


class UserBase(BaseModel): 
    username: str
    
class UserCreate(UserBase): 
    password: str

class UserOutBase(UserBase):
    id: UUID