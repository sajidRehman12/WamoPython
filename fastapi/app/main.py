from fastapi import FastAPI
from app.routers.users import router as userRouter
app=FastAPI()


app.include_router(userRouter)


@app.get("/")
def home():
    return {"message": "FastAPI is running"}

