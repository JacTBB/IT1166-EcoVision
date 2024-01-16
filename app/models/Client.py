from app.database import db
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column



class Location(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)

class Utility(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company: Mapped[int] = mapped_column(Integer)
    location: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    date: Mapped[Date] = mapped_column(Date)
    carbonfootprint: Mapped[str] = mapped_column(String)
    energyusage: Mapped[str] = mapped_column(String)
    waterusage: Mapped[str] = mapped_column(String)

class Assessment(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company: Mapped[int] = mapped_column(Integer)
    location: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    progress: Mapped[int] = mapped_column(Integer)