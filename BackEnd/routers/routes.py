from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Annotated
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from BackEnd.database import Session
from BackEnd.schema import UserCreate, FlashcardSetUpdate, FlashcardUpdate
from BackEnd.models import Flashcard, FlashcardSet

router = APIRouter()


@router.get("/")
def root(): 
    return {"Hello": "World"}

#add middleware and get user vvv
@router.update("/flashcards/set/{set_id},")
def update_flashcard_setname(set_id: int, set_title: FlashcardSetUpdate):
    stmt = (
        update(FlashcardSet)
        .where(FlashcardSet.id == set_id)
        .values(**set_title.model_dump(exclude_unset=True))
    )

#add middleware and get user vvv
@router.update("/flashcards/{set_id}/{flashcard_id}")
def update_flashcard(set_id: int, flashcard_id: int, flashcard_data: FlashcardUpdate):
    data = flashcard_data.model_dump()
    stmt = (
        update(flashcard_data)
        .where(Flashcard.set_id == set_id, Flashcard.id == flashcard_id)
        .values(**flashcard_data.model_dump(exclude_unset=True))
        )
    
    

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate): 
    data = user_data.model_dump()
    
    if not data["username"] or not data["password"]: 
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    hashed_pw = 
    
    
    with Session() as session:
        
        
        
    
