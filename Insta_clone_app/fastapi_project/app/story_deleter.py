# app/scheduler.py
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from app.database.database import SessionLocal
from app.models.tables import Story      
from sqlalchemy.orm import Session

def delete_stories(sessionFactory):
    db=sessionFactory()
    db.expire_all() 

    try:
        now = datetime.now().astimezone() 

        
        due_stories = db.query(Story).filter(
            Story.expires_at <= now
        ).all()
        print(due_stories)
        print("Story_deleter is running")
        if due_stories:
            for story in due_stories:
                print(f"[BACKGROUND] story ID {story.id}")
                db.delete(story)
            db.commit()
            
    except Exception as e:
        print(f"[BACKGROUND ERROR] Failed to delete story: {e}")
    finally:
        db.close()

def story_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_stories, 'interval', minutes=1, args=[SessionLocal])
    scheduler.start()
    print("[BACKGROUND] Scheduled post monitor started. Checking every 60 seconds.")
