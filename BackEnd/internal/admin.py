# BackEnd/internal/admin.py
from sqlalchemy.exc import IntegrityError
from BackEnd.database import Session
from BackEnd import models  # import your ORM models

def delete_all_flashcards():
    with Session() as session:
        try:
            session.execute(models.Flashcard.__table__.delete())
            session.commit()
        except IntegrityError:
            session.rollback()
            print("Error deleting flashcards")

def delete_all_flashcard_sets():
    with Session() as session:
        try:
            session.execute(models.FlashcardSet.__table__.delete())
            session.commit()
        except IntegrityError:
            session.rollback()
            print("Error deleting flashcard sets")

def delete_all_sessions():
    with Session() as session:
        try:
            session.execute(models.Active_Session.__table__.delete())
            session.commit()
        except IntegrityError:
            session.rollback()
            print("Error deleting sessions")

def delete_all_users():
    with Session() as session:
        try:
            session.execute(models.User.__table__.delete())
            session.commit()
        except IntegrityError:
            session.rollback()
            print("Error deleting users")


def reset_database():
    delete_all_flashcards()
    delete_all_flashcard_sets()
    delete_all_sessions()
    delete_all_users()
    print("Database reset complete: all users, sets, and cards removed.")


if __name__ == "__main__":
    reset_database()