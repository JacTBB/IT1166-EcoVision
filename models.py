from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, DATETIME
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Customer(db.Model):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"{self.username} {self.email} {self.password} {self.type}"


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String())
    password = db.Column(db.String())
    type = db.Column(db.String())

    def __repr__(self) -> str:
        return f"{self.username} {self.email} {self.password} {self.type}"


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String())
    password = db.Column(db.String())
    type = db.Column(db.String())

    def __repr__(self) -> str:
        return f"{self.username} {self.email} {self.password} {self.type}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String())
    author = db.Column(db.String())
    date: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.utcnow)
    image_name = db.Column(db.String())
    postid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"{self.title} {self.content} {self.author} {self.date} {self.image_name}"
