from typing import List
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from BackEnd.database import Base



class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    flashcard_sets: Mapped[List["FlashcardSet"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @staticmethod
    def to_string(id, username):
        return f"ID: {id}, USERNAME: {username}"


class FlashcardSet(Base):
    __tablename__ = "flashcard_sets"

    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="flashcard_sets")

    flashcards: Mapped[List["Flashcard"]] = relationship(
        back_populates="flashcard_set",
        cascade="all, delete-orphan"
    )

    @staticmethod
    def to_string(title):
        return f"TITLE: {title}"


class Flashcard(Base):
    __tablename__ = "flashcards"

    id: Mapped[str] = mapped_column(primary_key=True)
    front: Mapped[str] = mapped_column(nullable=False)
    back: Mapped[str] = mapped_column(nullable=False)

    flashcard_set_id: Mapped[str] = mapped_column(
        ForeignKey("flashcard_sets.id"),
        nullable=False
    )
    flashcard_set: Mapped["FlashcardSet"] = relationship(back_populates="flashcards")

    @staticmethod
    def to_string(front, back):
        return f"FRONT: {front}\nBACK: {back}"