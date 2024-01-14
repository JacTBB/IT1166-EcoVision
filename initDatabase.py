from app import create_app
from app.config import Config
from app.database import db
from app.models.User import Client, Author, Technician, Consultant, Manager, Admin
from app.models.News import Post
from app.models.Client import Location, Utility
from app.models.Company import Company
from datetime import datetime
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
            user.set_company(1)

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
    for i in range(1,3):
        company = Company(name=f"SomeCompanyName {i}",
                          industry="Industrial",
                          address="SG 1234",
                          email="company@gmail.com")
        db.session.add(company)
        
        for j in range(1, 3):
            location = Location(company=i, name=f"Office {j}", address="SG 1234")
            db.session.add(location)
            
            for k in range(1, 11):
                utility = Utility(company=i, location=j, name=f"Utility {k}", date=datetime(2024, k, 1),
                                carbonfootprint=randint(1,500), energyusage=randint(1,500), waterusage=randint(1,500))
                db.session.add(utility)
    
    
    
    db.session.commit()