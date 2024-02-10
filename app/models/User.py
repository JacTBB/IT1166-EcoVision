import uuid
from app.database import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


class User(db.Model, UserMixin):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String)
    profile_picture: Mapped[str] = db.Column(db.String())
    password_hash: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)

    def __init__(self, username, email, type):
        self.user_id = str(uuid.uuid4())
        self.first_name = "John"
        self.last_name = "Doe"
        self.username = username
        self.email = email
        self.phone_number = "00000000"
        self.profile_picture = "icon.jpg"
        self.type = type

    def get_id(self):
        return self.user_id

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)


class Client(User):
    company: Mapped[str] = mapped_column(String)

    def __init__(self, username, email):
        super().__init__(username, email, 'client')

    def set_company(self, company: str):
        self.company = company


class Author(User):
    def __init__(self, username, email):
        super().__init__(username, email, 'author')


class Technician(User):
    def __init__(self, username, email):
        super().__init__(username, email, 'technician')


class Consultant(User):
    def __init__(self, username, email):
        super().__init__(username, email, 'consultant')


class Manager(User):
    def __init__(self, username, email):
        super().__init__(username, email, 'manager')


class Admin(User):
    def __init__(self, username, email):
        super().__init__(username, email, 'admin')
