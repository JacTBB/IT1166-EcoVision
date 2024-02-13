from app.database import db
from sqlalchemy import Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column


class Chat(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company: Mapped[int] = mapped_column(Integer)
    messages = db.Column(JSON)
