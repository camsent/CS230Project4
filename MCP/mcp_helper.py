from BackEnd.database import Session
from BackEnd.models import User, FlashcardSet, Flashcard, Active_Session
from BackEnd.auth.auth import auth
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
import uuid
import json

current_user_id = None  # holds current logged-in user id


# ---------- USER AUTH ----------
def register_user(username: str, password: str) -> str:
    if not username or not password:
        return "Invalid username or password."

    hashed_pw = auth.hash_password(password)
    user_id = str(uuid.uuid4())

    with Session() as session:
        check = session.scalars(select(User).where(User.username == username)).first()
        if check:
            return "Username already taken."

        try:
            new_user = User(id=user_id, username=username, hashed_password=hashed_pw)
            session.add(new_user)
            session.commit()
            return f"User created successfully. ID: {user_id}"
        except IntegrityError:
            session.rollback()
            return "Database error creating user."


def login_user(username: str, password: str) -> str:
    global current_user_id

    with Session() as session:
        user = session.scalars(select(User).where(User.username == username)).first()
        if not user:
            return "User not found."

        if not auth.check_password(password, user.hashed_password):
            return "Incorrect password."

        sess_id = str(uuid.uuid4())
        try:
            new_sess = Active_Session(id=sess_id, user_id=user.id)
            session.add(new_sess)
            session.commit()
            current_user_id = user.id
            return f"Login successful. Session ID: {sess_id}"
        except IntegrityError:
            session.rollback()
            return "Login failed due to database error."


def logout_user() -> str:
    global current_user_id
    if not current_user_id:
        return "No user is currently logged in."
    with Session() as session:
        session.execute(delete(Active_Session).where(Active_Session.user_id == current_user_id))
        session.commit()
    current_user_id = None
    return "Logged out successfully."


# ---------- FLASHCARD MANAGEMENT ----------
def list_sets() -> str:
    if not current_user_id:
        return "You must be logged in."
    with Session() as session:
        sets = session.scalars(select(FlashcardSet).where(FlashcardSet.user_id == current_user_id)).all()
        if not sets:
            return "No flashcard sets found."
        return "\n".join([f"{s.id}: {s.title}" for s in sets])


def list_flashcards(set_id: str) -> str:
    if not current_user_id:
        return "You must be logged in."
    with Session() as session:
        flashcards = session.scalars(
            select(Flashcard).where(Flashcard.flashcard_set_id == set_id)
        ).all()
        if not flashcards:
            return "No flashcards found."
        return "\n\n".join([f"{f.id}\nFront: {f.front}\nBack: {f.back}" for f in flashcards])


def create_flashcard_set(title: str) -> str:
    if not current_user_id:
        return "You must be logged in."
    with Session() as session:
        try:
            set_id = str(uuid.uuid4())
            new_set = FlashcardSet(id=set_id, title=title, user_id=current_user_id)
            session.add(new_set)
            session.commit()
            return f"Set '{title}' created. ID: {set_id}"
        except IntegrityError:
            session.rollback()
            return "Set title already exists."


def create_flashcard(set_id: str, front: str, back: str) -> str:
    if not current_user_id:
        return "You must be logged in."
    with Session() as session:
        try:
            flash_id = str(uuid.uuid4())
            new_card = Flashcard(id=flash_id, front=front, back=back, flashcard_set_id=set_id)
            session.add(new_card)
            session.commit()
            return f"Flashcard created. ID: {flash_id}"
        except IntegrityError:
            session.rollback()
            return "Error creating flashcard."


def update_flashcard(set_id: str, flashcard_id: str, front: str = None, back: str = None) -> str:
    if not current_user_id:
        return "You must be logged in."
    with Session() as session:
        values = {}
        if front:
            values["front"] = front
        if back:
            values["back"] = back
        if not values:
            return "No updates provided."

        try:
            stmt = (
                update(Flashcard)
                .where(Flashcard.id == flashcard_id, Flashcard.flashcard_set_id == set_id)
                .values(**values)
            )
            result = session.execute(stmt)
            session.commit()
            if result.rowcount == 0:
                return "Flashcard not found."
            return "Flashcard updated successfully."
        except IntegrityError:
            session.rollback()
            return "Error updating flashcard."


def delete_flashcard(set_id: str, flashcard_id: str) -> str:
    if not current_user_id:
        return "You must be logged in."
    with Session() as session:
        result = session.execute(
            delete(Flashcard).where(Flashcard.id == flashcard_id, Flashcard.flashcard_set_id == set_id)
        )
        session.commit()
        if result.rowcount == 0:
            return "Flashcard not found."
        return "Flashcard deleted."


# ---------- EXPORT ----------
def export_flashcard_sets_to_json() -> str:
    """Export all flashcard sets and flashcards for the current user as JSON."""
    if not current_user_id:
        return "You must be logged in."

    with Session() as session:
        sets = session.scalars(
            select(FlashcardSet).where(FlashcardSet.user_id == current_user_id)
        ).all()

        if not sets:
            return "No flashcard sets found."

        data = []
        for s in sets:
            flashcards = session.scalars(
                select(Flashcard).where(Flashcard.flashcard_set_id == s.id)
            ).all()
            data.append({
                "set_id": s.id,
                "title": s.title,
                "flashcards": [
                    {"id": f.id, "front": f.front, "back": f.back}
                    for f in flashcards
                ],
            })

        return json.dumps(data, indent=4)