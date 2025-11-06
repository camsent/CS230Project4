from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Annotated
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from BackEnd.models import User, Active_Session
from BackEnd.schema import UserCreate
from BackEnd.database import Session
from BackEnd.auth import auth
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
def login(user_data: UserCreate):
    data = user_data.model_dump()
    
    str_password = str(data["password"])
    user = auth.check_user_id(data["username"])
    
    if not user: 
        raise HTTPException(401, "User does not exist")
    
    user = auth.get_user_data_at_login(data["username"])
    checked_pw = auth.check_password(str_password, user.hashed_password)
    
    if not checked_pw: 
       raise HTTPException(status_code=401, detail="User does not exist") 
   
    with Session() as session: 
       try: 
            sess_id = str(uuid.uuid4())
            
            new_session = Active_Session(
                id = sess_id,
                user_id = user.id
            )
            #session.execute(stmt)
            session.add(new_session)
            
            session.commit()
            
       except IntegrityError: 
            session.rollback()
            raise HTTPException(status_code=400, detail="Bad login request")
            
    return {
        "session_id": sess_id, 
        "user_id: ": user.id, 
        "message": "Login successful" 
    }   
            
        
        
        
        
    
