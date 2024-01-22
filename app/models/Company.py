from app.database import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column



class Company(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    industry: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    logo: Mapped[str] = db.Column(db.String())
    plan: Mapped[str] = mapped_column(String)
    
    payment_name: Mapped[str] = mapped_column(String, nullable=True)
    payment_card_no: Mapped[str] = mapped_column(String, nullable=True)
    payment_expiry: Mapped[str] = mapped_column(String, nullable=True)
    payment_cvc: Mapped[str] = mapped_column(String, nullable=True)