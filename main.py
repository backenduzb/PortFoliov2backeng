import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from authentication import authentication
from routers import user_routers
from routers.chat import global_router, private_router
from tortoise.contrib.fastapi import register_tortoise
from config import TORTOISE_ORM

app = FastAPI()

# Railway yoki o'z domenlaring
origins = [
    "http://localhost:5173",                  # Local dev
    "http://127.0.0.1:5173",                  # Local dev
    "https://myfrontend.com",                 # Agar frontend serverda bo'lsa
    "https://myapp.up.railway.app",
    "https://myportfolios-delta.vercel.app",            # Railway backend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Ruxsat berilgan domenlar
    allow_credentials=True,      # Cookie ishlashi uchun shart
    allow_methods=["*"],         # GET, POST va boshqalarga ruxsat
    allow_headers=["*"],         # Har qanday headerga ruxsat
)

# Routerlar
app.include_router(authentication.router)
app.include_router(user_routers.router)
app.include_router(global_router.router)
app.include_router(private_router.router)

# Tortoise ORM
register_tortoise(
    app,
    config=TORTOISE_ORM,  
    generate_schemas=True,
    add_exception_handlers=True
)

# Railway serverda ishlashi uchun
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
