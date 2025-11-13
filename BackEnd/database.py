from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

# Make sure "database" folder exists
os.makedirs(os.path.join(os.path.dirname(__file__), "database"), exist_ok=True)

# Absolute path for DB
db_path = os.path.join(os.path.dirname(__file__), "database", "database.db")

# Engine
engine = create_engine(f"sqlite:///{db_path}", echo=True)

# Base class
class Base(DeclarativeBase):
    pass

# Classic Session
Session = sessionmaker(engine)