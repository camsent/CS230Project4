from fastapi.middleware.cors import CORSMiddleware
from BackEnd import app
from BackEnd.routers import routes as core_routes
#from BackEnd.internal import admin as admin_routes

from dotenv import load_dotenv
import os

load_dotenv()

app.include_router(core_routes.router)




origins = ["http://localhost:5173"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)