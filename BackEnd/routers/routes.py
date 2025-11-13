from fastapi import APIRouter, Depends, HTTPException, status, Response, UploadFile, Form
from typing import Annotated
from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import IntegrityError

from BackEnd import UPLOAD_DIR
from BackEnd.models import User, Active_Session, FlashcardSet, Flashcard
from BackEnd.schema import UserCreate, FlashcardUpdate, FlashcardSetUpdate, FlashcardSetCreate
from BackEnd.database import Session
from BackEnd.auth import auth
from BackEnd.middleware import middleware
from BackEnd.internal import utils

import uuid
import json

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
            active_user = session.scalars(select(Active_Session).where(Active_Session.user_id == user.id)).first()
            if active_user: 
               raise HTTPException(status_code=400, detail="User already logged in")
           
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


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(user_id: Annotated[str, Depends(middleware.get_current_user)]):
    with Session() as session: 
        try: 
            stmt = delete(Active_Session).where(Active_Session.user_id == user_id)
            
            session.execute(stmt)
            session.commit()
        except IntegrityError: 
            raise HTTPException(status_code=400, detail="Error logging out user")
        
        return {"message": "Successful logout"}
        


@router.post("/upload")
async def create_upload_file(file: UploadFile, title: Annotated[str, Form()], user_id: Annotated[str, Depends(middleware.get_current_user)] ): # create_upload_files(files: list[UploadFile]) -> FOR MULTIPLE FILES IF NEEDED
    contents = await file.read()

    img_text = utils.extract_image_text(contents)
    flash_data = utils.create_flashcards(img_text)
    flash_data = flash_data.strip()
    flash_data = json.loads(flash_data)
    
    # for i in range(len(flash_data)): 
    #     print(flash_data[i])
    
    # Checking if set exists
    with Session() as session: 
        try: 
            flash_set = session.scalars(
                select(FlashcardSet)
                .where(FlashcardSet.title == title)
                .where(FlashcardSet.user_id == user_id)
                ).first()
        except IntegrityError: 
            raise HTTPException(status_code=400, detail="Error uploading flashcards")
            
        if not flash_set: 
            flash_set = create_flashcard_set(session, title, user_id)
            flash_set_id = flash_set.id
            
        else: 
            flash_set_id = flash_set.id
        
        try: 
            for i in range(len(flash_data)): 
                id = str(uuid.uuid4())
                new_flashcard = Flashcard(
                    id = id,
                    front = flash_data[i]["question"],
                    back = flash_data[i]["answer"],
                    flashcard_set_id = flash_set_id
                )
                session.add(new_flashcard)
                
            session.commit()
            
            return {
                "message": "Flashcards uploaded successfully",
                "set_id": flash_set.id,
                "num_flashcards": len(flash_data)
            }
        except IntegrityError: 
            raise HTTPException(status_code=400, detail="Error uploading flashcards")   
    
 
@router.get("/home")
def get_flashcard_sets(user_id: Annotated[str, Depends(middleware.get_current_user)]):
    with Session() as session:
        flashcard_sets = session.scalars(
            select(FlashcardSet).where(FlashcardSet.user_id == user_id)
        ).all()

        if not flashcard_sets:
            return {"message": "No flashcards"}

        result = []
        for fs in flashcard_sets:
            result.append({
                "id": fs.id,
                "title": fs.title
            })

        return result 
    

@router.get("/get/flashcard/set/{set_id}")
def get_flashcard_set(set_id: str, user_id: Annotated[str, Depends(middleware.get_current_user)]):
    with Session() as session: 
        flashcard_set = session.scalars(
            select(FlashcardSet)
            .where(FlashcardSet.id == set_id, FlashcardSet.user_id == user_id)
        ).first()
        
        if not flashcard_set: 
            raise HTTPException(status_code=404, detail="Flashcard set not found")
        
        flashcards = session.scalars(
            select(Flashcard)
            .where(Flashcard.flashcard_set_id == flashcard_set.id)
        ).all()
        
        result = {
            "set_id": flashcard_set.id,
            "title": flashcard_set.title,
            "flashcards": [
                {
                    "id": flashcard.id,
                    "front": flashcard.front,
                    "back": flashcard.back
                } for flashcard in flashcards
            ]
        }
        
        return result

@router.get("/get/flashcard/sets")
def get_flashcard_sets(user_id: Annotated[str, Depends(middleware.get_current_user)]):
    with Session() as session: 
        flashcard_sets = session.scalars(
            select(FlashcardSet)
            .where(FlashcardSet.user_id == user_id)
        ).all()
        
        result = []
        for flashcard_set in flashcard_sets: 
            flashcards = session.scalars(
                select(Flashcard)
                .where(Flashcard.flashcard_set_id == flashcard_set.id)
            ).all()
            
            result.append({
                "set_id": flashcard_set.id,
                "title": flashcard_set.title,
                "flashcards": [
                    {
                        "id": flashcard.id,
                        "front": flashcard.front,
                        "back": flashcard.back
                    } for flashcard in flashcards
                ]
            })
        
        return result            
        
#add middleware and get user vvv
#@router.patch("/flashcards/set/{set_id}")
#def update_flashcard_setname(set_id: int, set_title: FlashcardSetUpdate, user_id: Annotated[str, Depends(middleware.get_current_user)]):
    
#     with Session() as session: 
#         try: 
#             stmt = (
#                 update(FlashcardSet)
#                 .where(FlashcardSet.id == set_id)
#                 .where(FlashcardSet.user_id == user_id)
#                 .values(**set_title.model_dump(exclude_unset=True))
#             )
            
#             session.execute(stmt)
#             session.commit()
            
#         except IntegrityError: 
#             session.rollback()
#             raise HTTPException(status_code=400, detail="Error updating flashcard set title")
    

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
        
    


############################################################ ADMIN ##########################################################################
@router.get("/admin/active_users")
def get_active_users():
    with Session() as session: 
        try: 
            act_sessions = session.scalars(select(Active_Session)).all()
            if not act_sessions: 
                print("NO ACTIVE SESSIONS")
                return
            print("PRINTING USER SESSIONS ---------------------------------------------\n")
            
            for sess in act_sessions:
                print(sess.to_string(sess.id, sess.user_id))
           
            print("------------------------------------------------------------")
           
        except IntegrityError: 
            raise HTTPException(status_code=400, detail="Error getting active sessions")

@router.get("/admin/all-users")
def get_all_users():
    with Session() as session: 
        try: 
            users =  session.scalars(select(User)).all()
            if not users: 
                print("NO USERS")
                return
            print("PRINTING USERS ---------------------------------------------\n")
            
            for user in users:
                print(user.to_string(user.id, user.username))
           
            print("------------------------------------------------------------")
           
        except IntegrityError: 
            raise HTTPException(status_code=400, detail="Error getting active sessions")
        
        
        
###########################################    HELPER METHODS    ###############################################
        
def create_flashcard_set(session, set_title, user_id): 
        set_id = uuid.uuid4()
        try: 
           new_flashcard_set = FlashcardSet(
               id = str(uuid.uuid4()),
               title = set_title ,
               user_id = user_id,
           )
           
           session.add(new_flashcard_set)
           session.commit()
           
           print({"ID: ": set_id, "TITLE: ": set_title})
           return new_flashcard_set
        except IntegrityError: 
           session.rollback()
           raise HTTPException(status_code=400, detail="Error creating new flashcard set") 
        