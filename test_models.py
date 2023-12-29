from __init__ import db, app
from models import *

with app.app_context():
    # customer = Customer(username="test", email="email@gmail.com",
    #                     password="123", type="user")
    # db.session.add(customer)
    # db.session.commit()

    # Query user = User.query.filter_by(name='John Doe').first()

    query = db.session.query(Customer).filter_by(
        username="test").first()

    print(query.username)

    Customer = Customer.query.all()
    Author = Author.query.all()
    Admin = Admin.query.all()

    print(Customer)
    print(Author)
    print(Admin)

    pass
