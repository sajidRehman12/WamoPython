from uuid import UUID
from sqlalchemy.orm import Session ,selectinload ,joinedload 
from sqlalchemy import func  
from app.models.tables import User
from app.models.tables import Comment

# from app.models.post import Post
# from app.models.follow import Follow    
# from app.models.user import User
# from app.models.comment import Comment
# from app.models.token import Token
# from app.models.notification import Notification
# from app.models.like import Like 
# from app.models.comment import Comment
# from app.models.tables import User

class CommentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, comment: Comment):
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_by_id(self, comment_id: int):
        return (
            self.db.query(Comment)
            .filter(Comment.id == comment_id)
            .first()
        )

    def get_by_post(self, post_id: int):
       # 1. Fetch all comments for the post
        results = (self.db.query(Comment, User.username)
                .join(User, Comment.user_id == User.id)
                .filter(Comment.post_id == post_id)
                .order_by(Comment.created_at.asc()) # Ascending helps with nesting
                .all())

        # 2. Organize in Python
        comments_map = {}
        root_comments = []

        # First pass: map everything and initialize replies list
        for comment, username in results:
            comment_dict = {**comment.__dict__, "username": username, "replies": []}
            comments_map[comment.id] = comment_dict

        # Second pass: group them
        for comment_id, comment_dict in comments_map.items():
            parent_id = comment_dict.get('parent_id')
            if parent_id and parent_id in comments_map:
                comments_map[parent_id]["replies"].append(comment_dict)
            else:
                root_comments.append(comment_dict)

        return root_comments
        # seen = set()
        # comments = []
        # for c in result:
        #     if c.Comment.id not in seen:
        #         seen.add(c.Comment.id)
        #         comments.append(c)

        # return [
        #     {
        #         "id": comment.Comment.id,
        #         "post_id": comment.Comment.post_id,
        #         "user_id": comment.Comment.user_id,
        #         "body": comment.Comment.body,
        #         "parent_id": comment.Comment.parent_id,
        #         "created_at": comment.Comment.created_at,
        #         "username": comment.username,
        #         "replies": [
        #             {
        #                 "id": reply.id,
        #                 "post_id": reply.post_id,
        #                 "user_id": reply.user_id,
        #                 "body": reply.body,
        #                 "parent_id": reply.parent_id,
        #                 "created_at": reply.created_at,
        #                 "username": reply.author.username if reply.author else None
        #             }
        #             for reply in comment.Comment.replies
        #         ]
        #     }
        #     for comment in comments
        # ]

    def get_replies(self, parent_id: int):
        
        return (
            self.db.query(Comment)
            .filter(Comment.parent_id == parent_id)
            .all()
        )


    def delete(self, comment: Comment):
        self.db.delete(comment)
        self.db.commit()