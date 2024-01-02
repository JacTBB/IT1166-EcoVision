from app.database import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from flask_bcrypt import Bcrypt



bcrypt = Bcrypt()



class User(db.Model, UserMixin):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)



class Customer(User):
    pass



class Author(User):
    pass



class Admin(User):
    pass