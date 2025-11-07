from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from typing import Annotated
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from BackEnd.models import User, Active_Session, FlashcardSet, Flashcard
from BackEnd.schema import UserCreate, FlashcardUpdate, FlashcardSetUpdate
from BackEnd.database import Session
from BackEnd.auth import auth
from BackEnd.middleware import middleware
import uuid

router = APIRouter()


@router.get("/")
def root(): 
    return {"Hello": "World"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate): 
    data = user_data.model_dump()
    
    if not data["username"] or not data["password"]: 
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    hashed_pw = auth.hash_password(data["password"])
    user_id = uuid.uuid4()
    user_id = str(user_id)
    
    
    with Session() as session:
        check_username = session.scalars(select(User).where(User.id == data["username"])).first()
        
        if check_username: 
            raise HTTPException(status_code=400, detail="Username already taken")
        
        try:
            new_user = User(
                id=user_id,
                username=data["username"],
                hashed_password=hashed_pw,
            )
            session.add(new_user)
            session.commit()
            result = {"ID: ": user_id, "Username: ": data["username"]}
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=400, detail="Error: User ID collision, please try again")

    return result

@router.post("/login")
def login(user_data: UserCreate, response: Response):
    data = user_data.model_dump()
    
    user = auth.get_user_data_login(data["username"])
    if not user:
        raise HTTPException(status_code=401, detail="User does not exist")

    
    check_pw = auth.check_password(data["password"], user.hashed_password)
    
    if not check_pw: 
       raise HTTPException(status_code=401, detail="User does not exist") 
   
    with Session() as session: 
       try: 
            sess_id = str(uuid.uuid4())
            
            new_session = Active_Session(
                id = sess_id,
                user_id = user.id
            )
            session.add(new_session)
            
            session.commit()
            
            response.set_cookie(
                key="session_id",
                value=sess_id,
                httponly=True,   
                samesite="lax",   
                secure=True
            ) 
            
       except IntegrityError: 
            session.rollback()
            raise HTTPException(status_code=400, detail="Bad login request")
            
    return {"message": "Login successful", "user_id": user.id}

            
        
#add middleware and get user vvv
@router.patch("/flashcards/set/{set_id}")
def update_flashcard_setname(set_id: int, set_title: FlashcardSetUpdate, user_id: Annotated[str, Depends(middleware.get_current_user)]):
    
    with Session() as session: 
        try: 
            stmt = (
                update(FlashcardSet)
                .where(FlashcardSet.id == set_id, FlashcardSet.user_id == user_id)
                .values(**set_title.model_dump(exclude_unset=True))
            )
            
            session.execute(stmt)
            session.commit()
            
        except IntegrityError: 
            session.rollback()
            raise HTTPException(status_code=400, detail="Error updating flashcard set title")
    

#add middleware and get user vvv
@router.patch("/flashcards/set/{set_id}/flashcard/{flashcard_id}")
def update_flashcard(set_id: int, flashcard_id: int, flashcard_data: FlashcardUpdate, user_id: Annotated[str, Depends(middleware.get_current_user)]):
    with Session() as session: 
        try: 
            stmt = (
                update(flashcard_data)
                .where(Flashcard.set_id == set_id, Flashcard.id == flashcard_id, Flashcard)
                .values(**flashcard_data.model_dump(exclude_unset=True))
            )    
            
            session.execute(stmt)
            session.commit()    
            
        except IntegrityError: 
            session.rollback()
            raise HTTPException(status_code=400, detail="Error updating flashcard data")

@router.delete("/flashcards/set/{set_id}")
def delete_flashcard_set(set_id: int, user_id: Annotated[str, Depends(middleware.get_current_user)]):
    with Session() as session: 
        try: 
            stmt = (
                delete(FlashcardSet)
                .where(FlashcardSet.id == set_id, FlashcardSet.user_id == user_id)
            )
            
            session.execute(stmt)
            session.commit()
            
        except IntegrityError: 
            session.rollback()
            raise HTTPException(status_code=400, detail="Error deleting flashcard set")
        
    
