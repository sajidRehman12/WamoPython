from collections import defaultdict
from datetime import datetime

from sqlalchemy.orm import Session
from app.models.tables import User,Follow
from app.models.tables import Story

# from app.models.post import Post
# from app.models.follow import Follow    
# from app.models.user import User
# from app.models.comment import Comment
# from app.models.token import Token
# from app.models.notification import Notification
# from app.models.like import Like 
class StoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, story: Story):
        self.db.add(story)
        self.db.commit()
        self.db.refresh(story)
        return story

    def get_by_id(self, story_id: int):
        return (
            self.db.query(Story)
            .filter(Story.id == story_id)
            .first()
        )

    def get_active_stories(self):
        return (
            self.db.query(Story)
            .filter(Story.expires_at > datetime.now())
            .order_by(Story.created_at.desc())
            .all()
        )
    

    # def get_stories_of_followings(self,user_id):
    #     following_tuples = self.db.query(Follow.following_id).filter(Follow.follower_id == user_id).all()

    #     following_ids = [row[0] for row in following_tuples]

    #     if not following_ids:
    #         return None 

    #     stories = self.db.query(Story,User.username).join(User,Story.user_id == User.id).filter(
    #         Story.user_id.in_(following_ids)
    #     ).all()

    #     stories = [{
    #         "id": story.id,
    #         "user_id": story.user_id,
    #         "image_url": story.media_url,
    #         "created_at": story.created_at,
    #         "expires_at": story.expires_at,
    #         "username": username
    #     } for story, username in stories     ]
    #     return stories if stories else None
    


    def get_stories_of_followings(self, user_id):
        following_ids = [r[0] for r in self.db.query(Follow.following_id).filter(Follow.follower_id == user_id).all()]
        if not following_ids:
            return None 

        results = self.db.query(Story, User.username).join(User).filter(Story.user_id.in_(following_ids)).order_by(Story.created_at.desc()).all()
        if not results:
            return None

        user_groups = {} 
        
        for story, username in results:
            if username not in user_groups:
                user_groups[username] = []
            
            user_groups[username].append({
                "id": story.id,
                "user_id": story.user_id,
                "media_url": story.media_url,
                "media_type": story.media_type,
                "created_at": story.created_at,
            })

        final_output = []
        for username, stories in user_groups.items():
            final_output.append({
                "user_id": stories[0]["user_id"],
                "username": username,
                "stories": stories
            })
            
        return final_output
    def get_user_stories(self, user_id: int):
        return (
            self.db.query(Story)
            .filter(Story.user_id == user_id)
            .order_by(Story.created_at.desc())
            .all()
        )

    def delete(self, story: Story):
        self.db.delete(story)
        self.db.commit()