from app.database import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Rooms(db.Model):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    host_userid: Mapped[str] = mapped_column(
        String, nullable=False, unique=True)
    room_code: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False)
    messages: Mapped[str] = mapped_column(String, nullable=True)
    who_created_account_id: Mapped[int] = mapped_column(Integer)
    to_who_acount_id: Mapped[int] = mapped_column(Integer)
