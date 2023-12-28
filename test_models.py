from __init__ import db, app
from models import *

with app.app_context():
    # new_Admin = Admin(username="Admin", email="email@gmail.com",
    #                   password="123", type="admin")

    # db.session.add(new_Admin)
    # db.session.commit()

    # new_user = User(username="User", email="email@gmail.com",
    #                 password="123", type="user")
    # db.session.add(new_user)
    # db.session.commit()

    # Query user = User.query.filter_by(name='John Doe').first()

    query = User.query.filter_by(name='John Doe').first()

    User = User.query.all()
    Author = Author.query.all()
    Admin = Admin.query.all()

    print(User)
    print(Author)
    print(Admin)

    pass
