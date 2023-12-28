from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String())
    password = db.Column(db.String(), unique=True)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __repr__(self) -> str:
        return f"{self.username} {self.email}, {self.password}, {self.type}"


class Author(User):
    __mapper_args__ = {
        'polymorphic_identity': 'author',
    }

    def __repr__(self) -> str:
        return super().__repr__()


class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __repr__(self) -> str:
        return super().__repr__()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    content = db.Column(db.String(), unique=True)
    author = db.Column(db.String(), unique=True)
    date = db.Column(db.String(), unique=True)
    image_name = db.Column(db.String(), unique=True)

    def __repr__(self) -> str:
        return f"{self.title} {self.content} {self.author} {self.date} {self.image_name}"
