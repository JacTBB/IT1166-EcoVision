from app import create_app
from app.config import Config
from app.database import db
from app.models.User import Client, Author, Technician, Consultant, Manager, Admin
from app.models.News import Post

app = create_app(Config)

with app.app_context():
    UserList = {'client': Client, 'author': Author,
                'technician': Technician, 'consultant': Consultant,
                'manager': Manager, 'admin': Admin}
    for UserType in UserList:
        UserClass = UserList[UserType]

        user = UserClass(username=UserType)
        user.set_password('123')
        if UserType == 'client':
            user.set_company('SomeCompanyName')
        
        db.session.add(user)
        db.session.commit()



    for i in range(5):
        post = Post(title="test",
                    content="Lorem ipsum dolor sit amet consectetur Lorem ipsum dolor sit amet consecteteeeur",
                    author="test",
                    image_name="Cover-image-1-495x400.jpg",
                    postid=i+5)
        db.session.add(post)
        db.session.commit()
