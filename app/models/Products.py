from app.database import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Products(db.models):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String)
    product_description: Mapped[str] = mapped_column(String)
    product_price: Mapped[int] = mapped_column(Integer)
    product_image: Mapped[str] = mapped_column(String)
    productid: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False)
