from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)

    #relationships

    posts: Mapped[List["Post"]] = relationship(back_populates = "author")
    likes: Mapped[List["Like"]] = relationship(back_populates = "author_like")
    comments: Mapped[List["Comment"]] = relationship(back_populates = "author_comment")

    messages_sended: Mapped[List["Message"]] = relationship(foreign_keys = "Message.user_sender_id", back_populates = "user_sender")
    messages_recieved: Mapped[List["Message"]] = relationship(foreign_keys = "Message.user_sended_id", back_populates = "user_sended")

    following: Mapped[List["Follow"]] = relationship(foreign_keys = "Follow.follower_id", back_populates = "follower")
    followers: Mapped[List["Follow"]] = relationship(foreign_keys = "Follow.followed_id", back_populates = "followed")

    def serialize(self):
        return{
            "id": self.id,
            "email": self.email,
            "username": self.username
        }




class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    post_url: Mapped[str] = mapped_column(nullable=False)

    #foreing keys
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable = False)

    #relationships
    author: Mapped["User"] = relationship(back_populates = "posts")
    post_likes: Mapped[List["Like"]] = relationship(back_populates = "post_like")
    post_comments: Mapped[List["Comment"]] = relationship(back_populates = "post_comment")

    def serialize(self):
        return{
            "id": self.id,
            "description": self.description,
            "post_url": self.post_url,
            "author_id": self.author_id
        }


 
class Follow(db.Model):
    __tablename__ = "follow"

    id: Mapped[int] = mapped_column(primary_key=True)

    #foreign keys
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable = False)
    followed_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable = False)

    #relationships
    follower: Mapped["User"] = relationship(foreign_keys = [follower_id], back_populates = "following")
    followed: Mapped["User"] = relationship(foreign_keys = [followed_id], back_populates = "followers")

    def serialize(self):
        return{
            "id": self.id,
            "follower_id": self.follower_id,
            "follower_id": self.followed_id
        }



 
class Message(db.Model):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)

    #foreing keys
    user_sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable = False)
    user_sended_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable = False)

    #relationships
    user_sender: Mapped["User"] = relationship(foreign_keys = [user_sender_id], back_populates = "messages_sended")
    user_sended: Mapped["User"] = relationship(foreign_keys = [user_sended_id], back_populates = "messages_recieved")

    def serialize(self):
        return{
            "id": self.id,
            "text": self.text,
            "user_sender_id": self.user_sender_id,
            "user_sended_id": self.user_sended_id
        }



class Like(db.Model):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(primary_key=True)
    liked: Mapped[bool] = mapped_column(nullable=False, default = False)

    #foreing keys
    author_like_id:  Mapped[int] = mapped_column(ForeignKey("user.id"), nullable = False)
    post_like_id:  Mapped[int] = mapped_column(ForeignKey("post.id"), nullable = False)

    #relationships
    author_like: Mapped["User"] = relationship(back_populates = "likes")
    post_like: Mapped["Post"] = relationship(back_populates = "post_likes")

    def serialize(self):
        return{
            "id": self.id,
            "liked": self.liked,
            "author_like_id": self.author_like_id,
            "post_like_id": self.post_like_id
        }



class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)

    #foreing keys
    author_comment_id:  Mapped[int] = mapped_column(ForeignKey("user.id"), nullable = False)
    post_comment_id:  Mapped[int] = mapped_column(ForeignKey("post.id"), nullable = False)

    #relationships
    author_comment: Mapped["User"] = relationship(back_populates = "comments")
    post_comment: Mapped["Post"] = relationship(back_populates = "post_comments")

    def serialize(self):
        return{
            "id": self.id,
            "text": self.text,
            "author_comment_id": self.author_comment_id,
            "post_comment_id": self.post_comment_id
        }