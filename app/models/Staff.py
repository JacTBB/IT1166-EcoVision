from app.database import db
from sqlalchemy import Integer, String, Date, Float
from sqlalchemy.orm import Mapped, mapped_column



class Announcement(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String)
    date: Mapped[Date] = mapped_column(Date)