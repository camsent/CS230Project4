
from argon2 import PasswordHasher
from BackEnd.database import Session
from sqlalchemy import select
from BackEnd.models import User

from fastapi import Depends, HTTPException 
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from datetime import datetime, timedelta, timezone




################################
#     USER AUTHENTICATION      #
################################

SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer()

def create_token(user_id: str, expires_minutes: int = 20):
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {"sub": user_id, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token 


def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



################################
#          USER LOGIN          #
################################

ph = PasswordHasher()

def hash_password(pw: str): 
    return ph.hash(pw)


def check_password(pw: str, hashed_pw: str): 
    return ph.verify(hashed_pw, pw)


def check_user_id(username):
    with Session() as session:
        user = session.scalars(select(User).where(User.username == username)).first()
        if user:
            return True
        return False
    

def get_user_data_login(username):
    with Session() as session:
        user = session.scalars(select(User).where(User.username == username)).first()
    return user

def get_user_data(id):
    with Session() as session:
        user = session.scalars(select(User).where(User.id == id)).first()
    return user