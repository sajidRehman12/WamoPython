from fastapi import FastAPI
from app.routers.auth.auth import router as auth_router
from app.routers.post_routes.post import router as post_router
app=FastAPI()

@app.get("/")
def home():
    return {"response":"this is a response from fast api home page"}

app.include_router(post_router)
app.include_router(auth_router)