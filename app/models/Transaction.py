from app.database import db
from sqlalchemy import Integer, String, Date, Float
from sqlalchemy.orm import Mapped, mapped_column



class Transaction(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    date: Mapped[Date] = mapped_column(Date)
    price: Mapped[float] = mapped_column(Float)



class CarbonPurchase(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    date: Mapped[Date] = mapped_column(Date)
    offset: Mapped[int] = mapped_column(Integer)



class AssessmentTransaction(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company: Mapped[int] = mapped_column(Integer)
    assessment: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    date: Mapped[Date] = mapped_column(Date)
    price: Mapped[float] = mapped_column(Float)