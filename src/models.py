from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)

    children: Mapped[List["Post"]] = relationship(back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
        }
    



class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "link": self.link
        }

