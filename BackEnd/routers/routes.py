from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Annotated
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError


router = APIRouter()


@router.get("/")
def root(): 
    return {"Hello": "World"}


# @router.post("/register", status_code=status.HTTP_201_CREATED)
# def register()
