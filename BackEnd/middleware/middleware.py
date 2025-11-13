from fastapi import Request, HTTPException, Cookie
from sqlalchemy import select
from BackEnd.models import User, Active_Session
from BackEnd.database import Session


def get_current_user(session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(status_code=401, detail="No session cookie found")
    
    with Session() as db:
        active = db.scalar(
            select(Active_Session)
            .where(Active_Session.id == session_id)
        )
        
        if not active:
            raise HTTPException(status_code=403, detail="Invalid or expired session")
        
        return active.user_id
       
            
