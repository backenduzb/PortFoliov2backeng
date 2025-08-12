from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from authentication import authentication
from routers import user_routers
from routers.chat import global_router, private_router
from tortoise.contrib.fastapi import register_tortoise
from config import TORTOISE_ORM  

app = FastAPI()

origins = [
    "http://localhost:5173",  # Frontend
    "http://127.0.0.1:5173",  # Agar boshqa port ishlatsa
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Ruxsat berilgan domenlar
    allow_credentials=True,      # Cookie bilan ishlash uchun
    allow_methods=["*"],         # GET, POST va boshqalarga ruxsat
    allow_headers=["*"],         # Har qanday headerga ruxsat
)

app.include_router(authentication.router)
app.include_router(user_routers.router)
app.include_router(global_router.router)
app.include_router(private_router.router)

register_tortoise(
    app,
    config=TORTOISE_ORM,  
    generate_schemas=True,
    add_exception_handlers=True
)
