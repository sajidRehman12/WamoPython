from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from app.database.routes.auth import router
import os


app=FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key="mysecretkey"
)

load_dotenv()

secret = os.getenv("SECRET_KEY")
app.include_router(router)

