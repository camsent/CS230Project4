from typing import List
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from BackEnd.database import Base



class User(Base): 
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(unique=True, nullable=False)
    
    flashcard_set: Mapped[List["Flashcard_Set"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    
    @staticmethod
    def to_string(id, username): 
        return f"ID: {id}, USERNAME: {username}"
    
    
class Flashcard_Set(Base): 
    __tablename__ = "flashcard_sets"
    
    id: Mapped[str] = mapped_column(primary_key=True) 
    
    
    user: Mapped["User"] = relationship(back_populates="flashcard_set")
    flashcard: Mapped[List["Flashcard"]] = relationship(back_populates="flashcard_set", cascade="all, delete-orphan")
    
    @staticmethod
    def to_string(title): 
        return f"TITLE: {title}"

    
    
class Flashcard(Base): 
    __tablename__ = "flashcards"
    
    id: Mapped[str] = mapped_column(primary_key=True) 
    front: Mapped[str] = mapped_column(nullable=False)
    back: Mapped[str] = mapped_column(nullable=False)
    
    flashcard_set: Mapped["Flashcard_Set"] = relationship(back_populates="flashcard")
    
    @staticmethod
    def to_string(front, back): 
        return f"FRONT: {front}\nBACK: {back}"
    
    