from fastapi import FastAPI,Depends
from fastapi.staticfiles import StaticFiles
from app.routers.auth.auth import router as auth_router
from app.routers.post_routes.post import router as post_router
from app.routers.notification_routes.notifications import router as notificatin_router
from app.routers.comment_routes.comment import router as comment_router
from app.routers.story_routes.story import router as story_router
# from app.routers.reply_routes.r import router as reply_router
from app.routers.follow_routes.follow import router as follow_router
from app.routers.feed_routes.feed import router as feed_router
from app.routers.like_router.like import router as like_router
from app.routers.user_routes.user import router as user_router
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.posts_shedular import start_scheduler
from app.story_deleter import story_scheduler
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.routers.search.search import router as search_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    story_scheduler()
    yield

app=FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],                      
    allow_headers=["*"],                      
)

app.mount("/static/stories", StaticFiles(directory="stories"), name="stories_static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/profile_pictures", StaticFiles(directory="profile_pictures"), name="profile_pictures")
app.include_router(notificatin_router)
app.include_router(search_router)
app.include_router(post_router)
app.include_router(auth_router)
app.include_router(comment_router)
app.include_router(story_router)
app.include_router(feed_router)
app.include_router(like_router)
app.include_router(user_router)
app.include_router(follow_router)

# app.include_router(reply_router)
@app.get("/")
def home():
    return {"response":"this is a response from fast api home page"}