from fastapi import FastAPI
from BackEnd.database import Base, engine
from BackEnd import models
import os


app = FastAPI()

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
