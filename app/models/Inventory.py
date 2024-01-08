from app.database import db
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column



class Product(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer)