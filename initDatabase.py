from app import create_app
from app.config import Config
from app.database import db
from app.models.Rooms import Rooms
from app.models.User import Client, Author, Technician, Consultant, Manager, Admin
from app.models.News import Post
from app.models.Client import Location, Utility, Assessment, Document
from app.models.Company import Company
from datetime import datetime
from random import randint
import json

app = create_app(Config)

with app.app_context():

    db.drop_all()
    db.create_all()

    rooms = Rooms(host_userid=json.dumps([1]), room_code=1234)
    db.session.add(rooms)

    # Users
    UserList = {'client': Client, 'author': Author,
                'technician': Technician, 'consultant': Consultant,
                'manager': Manager, 'admin': Admin}
    for UserType in UserList:
        UserClass = UserList[UserType]

        if UserType != 'client':
            user = UserClass(username=UserType)
            user.set_password('123')

            db.session.add(user)

    # Main
    rand = randint(1, 2)
    for i in range(1, 10):
        post = Post(title="test",
                    content="Lorem ipsum dolor sit amet consectetur Lorem ipsum dolor sit amet consecteteeeur",
                    author="test",
                    image_name="Cover-image-1-495x400.jpg",
                    postid=i*2)
        post.post_type = "News" if i % rand == 0 else "Insights"
        db.session.add(post)

    # Client
    countLocation = 0
    for i in range(1, 3):
        user = Client(username=f"client{i}")
        user.set_password('123')
        user.set_company(i)
        db.session.add(user)

        company = Company(name=f"SomeCompanyName {i}",
                          industry="Industrial",
                          address="SG 1234",
                          email="company@gmail.com",
                          plan="free")
        db.session.add(company)

        for j in range(1, 3):
            countLocation += 1
            location = Location(
                company=i, name=f"Office {j}", address="SG 1234")
            db.session.add(location)

            for k in range(1, 13):
                utility = Utility(company=i, location=countLocation, name=f"Utility {k}", date=datetime(2023, k, 1),
                                  carbonfootprint=randint(200, 500), energyusage=randint(200, 500), waterusage=randint(200, 500))
                db.session.add(utility)

    for i in range(3, 5):
        user = Client(username=f"client{i}")
        user.set_password('123')
        user.set_company(i)
        db.session.add(user)

        company = Company(name=f"SomeLargeCompanyName {i}",
                          industry="Industrial",
                          address="SG 1234",
                          email="company@gmail.com",
                          plan="custom")
        db.session.add(company)

        for j in range(1, 4):
            countLocation += 1
            location = Location(
                company=i, name=f"Office {j}", address="SG 1234")
            db.session.add(location)

            for k in range(1, 13):
                utility = Utility(company=i, location=countLocation, name=f"Utility 2022 {k}", date=datetime(2022, k, 1),
                                  carbonfootprint=randint(200, 500), energyusage=randint(200, 500), waterusage=randint(200, 500))
                db.session.add(utility)

            for k in range(1, 13):
                utility = Utility(company=i, location=countLocation, name=f"Utility 2023 {k}", date=datetime(2023, k, 1),
                                  carbonfootprint=randint(200, 500), energyusage=randint(200, 500), waterusage=randint(200, 500))
                db.session.add(utility)

        for j in range(1, 3):
            documents = []
            for k in range(1, 4):
                documents.append(k)
                document = Document(company=i, name=f"Document {k}", created=datetime(2023, j, 1), updated=datetime(2023, j, 2),
                                    content="Lorem ipsum dolor sit amet consectetur Lorem ipsum dolor sit amet consecteteeeur")
                db.session.add(document)

            assessment = Assessment(company=i, location=f"SG {j}", name=f"Office {j}", type="Environmental Impact Assessment",
                                    start_date=datetime(2023, j, 1), progress=20, documents=documents)
            db.session.add(assessment)

    db.session.commit()
