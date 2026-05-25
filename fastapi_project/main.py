from fastapi import FastAPI , Depends , BackgroundTasks , APIRouter
from pydantic import BaseModel
from routers import users
from wbs import router as wbrouter
from middlewares.auth_middleware import AuthMiddleware

app = FastAPI()
app.add_middleware(AuthMiddleware)




@app.get("/")
def home():
    return {"mvessage": "Hello FastAPI"}

app.include_router(wbrouter)
app.include_router(users.router)
