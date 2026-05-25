from fastapi import FastAPI ,UploadFile , File
from app.routers.users import router as userRouter
app=FastAPI()


app.include_router(userRouter)



@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    content = await file.read()

    with open(file.filename, "wb") as f:
        f.write(content)

    return {"filename": file.filename}


# @app.get("/stream")
# def streamResponse():
#     with open()



@app.get("/")
def home():
    return {"message": "FastAPI is running"}

