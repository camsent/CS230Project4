from fastapi import FastAPI
from BackEnd.database import Base, engine
from BackEnd import models

app = FastAPI()

Base.metadata.create_all(bind=engine)