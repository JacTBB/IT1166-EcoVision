from app import create_app
from app.config import Config
from app.database import db
from app.models.User import Customer, Admin
from app.models.News import Post

app = create_app(Config)

with app.app_context():
    customer = Customer(username="test")
    customer.set_password('123')
    db.session.add(customer)
    db.session.commit()

    admin = Admin(username="admin")
    admin.set_password('123')
    db.session.add(admin)
    db.session.commit()

    for i in range(5):
        post = Post(title="test", content="Lorem ipsum dolor sit amet consectetur Lorem ipsum dolor sit amet consecteteeeur", author="test",
                    image_name="Cover-image-1-495x400.jpg", postid=i+5)
        db.session.add(post)
        db.session.commit()
