from app.database import db
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String())
    author = db.Column(db.String())
    date: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.utcnow)
    image_name = db.Column(db.String())
    postid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)