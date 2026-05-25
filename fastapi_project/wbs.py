
from fastapi import FastAPI , WebSocket , APIRouter
from datetime import datetime
import asyncio
router= APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")
    time = datetime.now().minute
    print(time)

    async def every_2_minutes():
        while True:
            await asyncio.sleep(120) 
            await websocket.send_text(" 2 minutes passed notification")
        
    asyncio.create_task(every_2_minutes())

    while True:

        print("hello")
        data = await websocket.receive_text()
        print("Received:", data)
        if data == "bye":
            await websocket.send_text("Closing connection...")
            await websocket.close()
            break
