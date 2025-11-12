from fastapi.middleware.cors import CORSMiddleware
from BackEnd import app
from BackEnd.routers import routes as core_routes
#from BackEnd.internal import admin as admin_routes


app.include_router(core_routes.router)
#app.include_router(admin_routes.router)




origins = [
    "http://localhost:5174"
]


app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)