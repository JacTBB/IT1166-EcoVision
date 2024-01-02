from datetime import datetime
import flask_login
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, DATETIME
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash


class Base(DeclarativeBase):
    pass


db = SQLAlchemy()


class User(db.Model, flask_login.UserMixin):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Customer(User):
    pass


class Author(User):
    pass


class Admin(User):
    pass


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String())
    author = db.Column(db.String())
    date: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.utcnow)
    image_name = db.Column(db.String())
    postid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
