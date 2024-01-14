from app.database import db
from sqlalchemy import Integer, DateTime, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String(), nullable=True)
    author = db.Column(db.String())
    date: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.utcnow)
    image_name: Mapped[str] = mapped_column(String)
    postid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    featured_post: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)
