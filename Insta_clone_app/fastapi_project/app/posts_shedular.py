# app/scheduler.py
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from app.database.database import SessionLocal
from app.models.tables import Post      
from sqlalchemy.orm import Session

def check_and_publish_posts(sessionFactory):
    db=sessionFactory()
    db.expire_all()  # Pull fresh data from the disk

    try:
        now = datetime.now().astimezone() 

        
        due_posts = db.query(Post).filter(
            Post.is_published == False,
            Post.scheduled_at <= now
        ).all()
        print(due_posts)
        print("posts publisher is running")
        if due_posts:
            for post in due_posts:
                post.is_published = True
                print(f"[BACKGROUND] Publishing post ID {post.id}: {post.caption}")
            
            db.commit()
            
    except Exception as e:
        print(f"[BACKGROUND ERROR] Failed to run publish job: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_publish_posts, 'interval', minutes=1,args=[SessionLocal])
    scheduler.start()
    print("[BACKGROUND] Scheduled post monitor started. Checking every 60 seconds.")
