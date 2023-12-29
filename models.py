from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Customer(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String, unique=True)
    type: Mapped[str] = mapped_column(String, unique=True)

    def __repr__(self) -> str:
        return f"{self.username} {self.email} {self.password} {self.type}"


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), unique=True)
    type = db.Column(db.String(), unique=True)

    def __repr__(self) -> str:
        return f"{self.username} {self.email} {self.password} {self.type}"


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), unique=True)
    type = db.Column(db.String(), unique=True)

    def __repr__(self) -> str:
        return f"{self.username} {self.email} {self.password} {self.type}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    content = db.Column(db.String(), unique=True)
    author = db.Column(db.String(), unique=True)
    date = db.Column(db.String(), unique=True)
    image_name = db.Column(db.String(), unique=True)

    def __repr__(self) -> str:
        return f"{self.title} {self.content} {self.author} {self.date} {self.image_name}"
