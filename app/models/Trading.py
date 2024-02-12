from app.database import db
from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column



class Projects(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    stock: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    content = db.Column(db.String())
    carousel = db.Column(JSON)