from app import create_app
from app.config import Config
from app.database import db
from app.models.User import Client, Author, Technician, Consultant, Manager, Admin
from app.models.News import Post
from app.models.Client import Location, Utility
from datetime import date
from random import randint

app = create_app(Config)

with app.app_context():

    # Users
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



    # Main
    for i in range(1, 10):
        post = Post(title="test",
                    content="Lorem ipsum dolor sit amet consectetur Lorem ipsum dolor sit amet consecteteeeur",
                    author="test",
                    image_name="Cover-image-1-495x400.jpg",
                    postid=i*2)
        db.session.add(post)
        
    
    
    # Client
    for i in range(1, 3):
        location = Location(name=f"Office {i}", address="SG 1234")
        db.session.add(location)
        
        for j in range(1, 11):
            utility = Utility(location=i, name=f"Utility {j}", date=date(2024, j, 1),
                            carbonfootprint=randint(1,500), energyusage=randint(1,500), waterusage=randint(1,500))
            db.session.add(utility)
    
    
    
    db.session.commit()