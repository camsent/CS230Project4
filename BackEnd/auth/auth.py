
from argon2 import PasswordHasher
from BackEnd.database import Session
from sqlalchemy import select
from BackEnd.models import User


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