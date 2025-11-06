from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Annotated
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from BackEnd.schema import UserCreate
from BackEnd.database import Session

router = APIRouter()


@router.get("/")
def root(): 
    return {"Hello": "World"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate): 
    data = user_data.model_dump()
    
    if not data["username"] or not data["password"]: 
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    hashed_pw = 
    
    
    with Session() as session:
        
        
        
    
