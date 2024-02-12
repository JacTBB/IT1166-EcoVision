from app import create_app
from app.config import Config
from app.database import db
from app.models.Rooms import Rooms
from app.models.User import Client, Author, Technician, Consultant, Manager, Admin
from app.models.News import Post
from app.models.Client import Location, Utility, Assessment, Document
from app.models.Company import Company
from app.models.Trading import Projects
from datetime import datetime
from random import randint
import json

app = create_app(Config)

with app.app_context():

    db.drop_all()
    db.create_all()

    rooms = Rooms(host_userid=json.dumps(
        [1]), room_code=1234, who_created_account_id=0, to_who_acount_id=1)

    db.session.add(rooms)
    # Users
    UserList = {'client': Client, 'author': Author,
                'technician': Technician, 'consultant': Consultant,
                'manager': Manager, 'admin': Admin}
    for UserType in UserList:
        UserClass = UserList[UserType]

        if UserType != 'client':
            user = UserClass(username=UserType, email=f"{
                             UserType}_ecovision@jactbb.com")
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
        user = Client(username=f"client{i}", email=f"client{i}@email.com")
        user.set_password('123')
        user.set_company(i)
        db.session.add(user)

        company = Company(name=f"SomeCompanyName {i}",
                          industry="Industrial",
                          email="jactbb@jactbb.com",
                          phone_number="65501234",
                          address="SG 1234",
                          logo="icon.jpg",
                          plan="free")
        db.session.add(company)

        for j in range(1, 3):
            countLocation += 1
            location = Location(
                company=i, name=f"Office {j}", address="SG 1234")
            db.session.add(location)

            for k in range(1, 13):
                energy = randint(200, 500) * 0.5 / 1000
                water = waterusage = randint(200, 500) * 0.2 / 1000
                carbon = round(energy + water, 5)
                utility = Utility(company=i, location=countLocation, name=f"Utility {k}", date=datetime(2023, k, 1),
                                  carbonfootprint=carbon, energyusage=energy, waterusage=water)
                db.session.add(utility)

    for i in range(3, 5):
        user = Client(username=f"client{i}", email=f"client{i}@jactbb.com")
        user.set_password('123')
        user.set_company(i)
        db.session.add(user)

        company = Company(name=f"SomeLargeCompanyName {i}",
                          industry="Industrial",
                          email="jactbb@jactbb.com",
                          phone_number="65501234",
                          address="SG 1234",
                          logo="icon.jpg",
                          plan="custom")
        db.session.add(company)

        for j in range(1, 4):
            countLocation += 1
            location = Location(
                company=i, name=f"Office {j}", address="SG 1234")
            db.session.add(location)

            for k in range(1, 13):
                energy = randint(200, 500) * 0.5 / 1000
                water = waterusage = randint(200, 500) * 0.2 / 1000
                carbon = round(energy + water, 5)
                utility = Utility(company=i, location=countLocation, name=f"Utility 2022 {k}", date=datetime(2022, k, 1),
                                  carbonfootprint=carbon, energyusage=energy, waterusage=water)
                db.session.add(utility)

            for k in range(1, 13):
                energy = randint(200, 500) * 0.5 / 1000
                water = waterusage = randint(200, 500) * 0.2 / 1000
                carbon = round(energy + water, 5)
                utility = Utility(company=i, location=countLocation, name=f"Utility 2023 {k}", date=datetime(2023, k, 1),
                                  carbonfootprint=carbon, energyusage=energy, waterusage=water)
                db.session.add(utility)

        countDocument = 0
        for j in range(1, 3):
            documents = []
            for k in range(1, 4):
                countDocument += 1
                document = Document(company=i, name=f"Document {j}-{k}", assessment=j, created=datetime(2023, j, 1), updated=datetime(2023, j, 2),
                                    content="Lorem ipsum dolor sit amet consectetur Lorem ipsum dolor sit amet consecteteeeur")
                documents.append(countDocument)
                db.session.add(document)

            assessment = Assessment(company=i, location=f"SG {j}", name=f"Office {j}", type="Environmental Impact Assessment",
                                    start_date=datetime(2023, j, 1), progress=20, documents=documents)
            db.session.add(assessment)

    # Projects
    for i in range(0, 3):
        types = ['Conservation', 'Renewable', 'Methane']
        content = """
        In the heart of the lush Amazon rainforest, nestled amidst towering trees and teeming biodiversity, a Groundbreaking Conservation Project unfolds. Led by a dedicated team of environmentalists, scientists, and local communities, this Ambitious Initiative aims to safeguard the rich biological heritage of the Amazon basin while addressing the pressing challenges of deforestation, habitat loss, and climate change. Through a multi-faceted approach that blends scientific research, community engagement, and sustainable practices, the Project seeks to create a harmonious balance between human development and environmental conservation.

From establishing protected areas and wildlife corridors to implementing reforestation and agroforestry initiatives, Every Effort is made to safeguard the delicate ecosystems of the Amazon and promote the well-being of its inhabitants. Empowering local communities to become stewards of their natural resources, the Project fosters a sense of ownership and responsibility, ensuring that conservation efforts are not only effective but also inclusive and equitable. By harnessing the collective wisdom of indigenous peoples, traditional knowledge, and modern science, this Conservation Project represents a beacon of hope in the face of ecological challenges, offering a glimpse into a future where humans and nature thrive in harmony, hand in hand, amidst the verdant splendor of the Amazon rainforest.
        """
        project = Projects(name=f"Project {i+1}", type=types[i], stock=randint(
            1000, 10000), price=randint(200, 400), content=content)
        db.session.add(project)

    db.session.commit()
