from app.database import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column



class Location(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)