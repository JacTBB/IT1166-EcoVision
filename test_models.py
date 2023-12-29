from app import db, app
from models import *

with app.app_context():
    # customer = Customer(username="test", email="email@gmail.com",
    #                     password="123", type="user")
    # db.session.add(customer)
    # db.session.commit()

    # Query user = User.query.filter_by(name='John Doe').first()

    query = db.session.query(Customer).filter_by(
        username="test").first()

    if query is not None:
        print(query.username)

    for i in range(5):
        post = Post(title="test", content="Lorem ipsum dolor sit amet consectetur Lorem ipsum dolor sit amet consecteteeeur", author="test",
                    image_name="Cover-image-1-495x400.jpg", postid=i+5)
        db.session.add(post)
        db.session.commit()
