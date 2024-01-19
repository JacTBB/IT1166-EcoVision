import uuid
from app.database import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from flask_bcrypt import Bcrypt



bcrypt = Bcrypt()



class User(db.Model, UserMixin):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    
    def __init__(self, username, type):
        self.user_id = str(uuid.uuid4())
        self.username = username
        self.type = type
    
    def get_id(self):
        return self.user_id

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)



class Client(User):
    company: Mapped[str] = mapped_column(String)
    
    def __init__(self, username, company):
        super().__init__(username, 'client')
        self.company = company

    def set_company(self, company):
        self.company = company

    def get_company(self):
        return self.company


class Author(User):
    def __init__(self, username):
        super().__init__(username, 'author')

class Technician(User):
    def __init__(self, username):
        super().__init__(username, 'technician')
class Consultant(User):
    def __init__(self, username):
        super().__init__(username, 'consultant')

class Manager(User):
    def __init__(self, username):
        super().__init__(username, 'manager')
class Admin(User):
    def __init__(self, username):
        super().__init__(username, 'admin')