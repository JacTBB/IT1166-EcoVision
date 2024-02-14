from app import create_app
from app.config import Config
from app.database import db
# from app.models.Rooms import Rooms
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


    
    # Users
    UserList = {'client': Client, 'author': Author,
                'technician': Technician, 'consultant': Consultant,
                'manager': Manager, 'admin': Admin}
    Usernames = {
        'author': 'Amy',
        'technician': 'Ted',
        'consultant': 'Clint',
        'manager': 'Miguel',
        'admin': 'admin',
    }
    for UserType in UserList:
        UserClass = UserList[UserType]

        if UserType != 'client':
            email = f"{UserType}@jactbb.com"
            user = UserClass(username=Usernames[UserType], email=email)
            user.set_password('123')

            db.session.add(user)

    # Main
    rand = randint(1, 2)
    for i in range(1, 10):
        post = Post(title="test",
                    content="Lorem ipsum dolor sit amet consectetur Lorem ipsum dolor sit amet consecteteeeur",
                    author=f"Test {i}",
                    image_name="Cover-image-1-495x400.jpg",
                    postid=i*2)
        post.post_type = "News" if i % rand == 0 else "Insights"
        db.session.add(post)
    
    post1 = Post(title="COP28 Global Offshore",
                content="""
Over the last year, there has been a notable increase in policy development aimed at bolstering offshore wind energy, with auctions escalating since COP27. The major inflection point has been China overtaking the birthplace of offshore wind – Europe – in total operational capacity.
Despite China's growth, Europe's North Sea regions, including the UK, Germany, the Netherlands, and Denmark, have maintained their growth trajectories, with heightened targets and significant auctions.<br><br>
Early-stage project development increased 34% from markets all around the world. Emerging frameworks in the Mediterranean and Baltic Seas in Europe, and new markets from Australia to Brazil and the Philippines outside of Europe have shown considerable portfolio growth.<br><br>
Developers remain keen to continue their long-term growth plans despite the current 40% cost increase from interest rate hikes, inflation, and supply chain issues. Disruption has mostly affected medium term projects due to be constructed before the end of the decade.
Examples include in the UK where no capacity in the Annual Allocation Round (AR5) was awarded a route to market, in the US, where multiple offtake contracts are being re-negotiated and terminated, and in Poland, where developers are delaying project FIDs.<br><br>
Despite this growth, offshore wind deployment is far behind the capacity calculated to reach net-zero. With the total amount of global operational offshore wind capacity projected to be up to 250 GW by 2030, this is inadequate to meet IRENA's almost 500 GW by 2030 recommendation for net-zero scenarios.<br><br>
With proven technology, investor interest, and a substantial project pipeline, the foundations for offshore wind expansion are set. Yet, critical challenges persist, such as permitting, grid integration, supply chain issues, and financial support.<br><br>
Tackling these obstacles requires urgent collaborative efforts from governments, industry, and civil society.
There are various policy mechanisms at our disposal today that could mitigate these issues. By adopting best practices from global leaders in offshore wind, we can bridge the gap and ensure that offshore wind plays a pivotal role in combating climate change.
""",
                author="test",
                image_name="Cover-image-1-495x400.jpg",
                postid=11*2)
    post1.post_type = "News"
    db.session.add(post1)



    # Client
    countLocation = 0
    for i in range(1, 3):
        user = Client(username=f"client{i}", email=f"client{i}@jactbb.com")
        user.set_password('123')
        user.set_company(i)
        db.session.add(user)

        company = Company(name=f"SomeCompanyName {i}",
                          industry="Industrial",
                          email=f"company{i}@jactbb.com",
                          phone_number="65501234",
                          address="SG 123456",
                          logo="icon.jpg",
                          plan="free")
        db.session.add(company)

        for j in range(1, 3):
            countLocation += 1
            location = Location(
                company=i, name=f"Office {j}", address="SG 123456")
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
                          email=f"company{i}@jactbb.com",
                          phone_number="65501234",
                          address="SG 123456",
                          logo="icon.jpg",
                          plan="custom")
        db.session.add(company)

        for j in range(1, 4):
            countLocation += 1
            location = Location(
                company=i, name=f"Office {j}", address="SG 123456")
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
                
            if j == 1:
                countDocument += 1
                document1 = Document(company=i, name=f"Document Assessment", assessment=j, created=datetime(2023, j, 1), updated=datetime(2023, j, 2),
                                    content="""
<div id="doc"><div class="et_pb_row et_pb_row_0"> <div class="et_pb_column et_pb_column_4_4 et_pb_column_0  et_pb_css_mix_blend_mode_passthrough et-last-child"> <div class="et_pb_module et_pb_text et_pb_text_1  et_pb_text_align_left et_pb_bg_layout_light"> <div class="et_pb_text_inner"> <h2><span class="EOP SCXW153554819 BCX0" data-ccp-props="{&quot;134233117&quot;:true,&quot;134233118&quot;:true,&quot;335551550&quot;:6,&quot;335551620&quot;:6,&quot;335559738&quot;:200,&quot;335559739&quot;:200}">About the Project</span></h2> </div> </div> <div class="et_pb_module et_pb_text et_pb_text_2  et_pb_text_align_left et_pb_bg_layout_light"> <div class="et_pb_text_inner"> <p><a href="https://www.pub.gov.sg/news/pressreleases/PUBandSembcorpCommenceConstructionof60MWPFloatingSolarPhotovoltaicSystemonTengehReservoir">PUB</a>, Singapore’s National Water Agency, in collaboration with&nbsp;<a href="https://www.sembcorp.com/en/media/media-releases/energy/2021/july/sembcorp-and-pub-officially-open-the-sembcorp-tengeh-floating-solar-farm/">Sembcorp</a>, energy and urban developer, has undertaken to build a floating solar photovoltaic (PV) system of 60 MWP (Megawatt peak) at Tengeh Reservoir.</p> <p>The Tengeh Reservoir floating solar farm is Singapore’s largest, and one of the largest in the world. It covers a massive area equivalent to 45 football fields. Its carbon savings are equivalent to taking 7000 cars off the roads. Clean and operating silently, PV systems have developed from being niche market applications into a mature technology used for mainstream power generation.</p> </div> </div> <div class="et_pb_module et_pb_text et_pb_text_3 et_clickable  et_pb_text_align_left et_pb_bg_layout_light"> <div class="et_pb_text_inner"> <h2><strong>Our Approach</strong></h2> </div> </div> <div class="et_pb_module et_pb_text et_pb_text_4  et_pb_text_align_left et_pb_bg_layout_light"> <div class="et_pb_text_inner"> <p>ESC, as the leading environmental consultant in the region in renewable energy and sustainability, is proud to be part of the process offering our expertise in the field of Environmental Impact Assessments (EIA) and Environmental Impact Study (EIS). Together with PUB, we have developed purpose-fit, strategic environmental solutions to support the completion of this project.&nbsp;</p> <p>Our scope of work involved evaluating the potential impacts that installing the solar PV system has on the water quality, on the flora and fauna of the reservoir, biodiversity, air quality, and noise amongst others. Further water quality simulation study was recommended to optimise the floating solar panel configurations as well as Environmental Monitoring and Management Plan (EMMP) for the pre, during, and post-construction of the project.</p> <p>The preparation for the EMMP requirements involved extensive biodiversity survey work including camera trapping which focused on the presence and behaviour of birds and otters within the reservoir, to determine any long-term environmental impacts to the fauna.</p> </div> </div> <div class="et_pb_module et_pb_image et_pb_image_0"><span class="et_pb_image_wrap "><img src="https://media.istockphoto.com/id/1394781347/photo/hand-holdig-plant-growing-on-green-background-with-sunshine.webp?b=1&amp;s=170667a&amp;w=0&amp;k=20&amp;c=Y-WUjWLqDY4y78qe_3ZtoVzAIGDYdxP3c5UXGnna64o=" alt="350+ Environment Pictures [HQ] | Download Free Images &amp; Stock Photos on  Unsplash"></span></div> <div class="et_pb_module et_pb_text et_pb_text_5  et_pb_text_align_left et_pb_bg_layout_light"> <div class="et_pb_text_inner"> <p><em>ESC Group Director Andrew Young and Operations Manager (Projects) Jessie Nguyen at the Opening Ceremony at Tengeh Reservoir Solar Farm</em></p> </div> </div> <div class="et_pb_module et_pb_text et_pb_text_6  et_pb_text_align_left et_pb_bg_layout_light"> <div class="et_pb_text_inner"> <h2>Outcome</h2> </div> </div> <div class="et_pb_module et_pb_text et_pb_text_7  et_pb_text_align_left et_pb_bg_layout_light"> <div class="et_pb_text_inner"> <p>The Tengeh Reservoir solar PV system is just one of several renewable energy development projects which are driving Singapore towards more sustainable methods of energy production. In land-scarce Singapore, the large surface areas of reservoirs present great potential for solar energy generation. ESC is privileged to offer its expertise and experience as Singapore powers its way towards its 2030 solar energy target.</p> <p>Working with PUB and design team during the environmental impact study (EIS) stage, as well as SembCorp in the construction and operations phases, ESC’s environmental experts have made a valuable contributions towards decarbonizing Singapore’s energy supply whilst providing innovations considerations to minimize potential impacts to reservoir water quality and the environment. To date, the ESC team has advised and assisted numerous renewables developers across Asia, to install more than 2.5GW of Solar and Wind power.</p> </div> </div> </div> </div> <div class="et_pb_row">&nbsp;</div></div>
""")
                documents.append(countDocument)
                db.session.add(document1)

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
        carousel = [
            "https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/69214561/3/?bust=1696792028&width=720",
            "https://images.livemint.com/img/2023/12/07/1140x641/dog-4615198_1280_1701927561029_1701927572424.jpg"
        ]
        project = Projects(name=f"Project {i+1}", type=types[i], stock=randint(
            1000, 10000), price=randint(200, 400), content=content, carousel=carousel)
        db.session.add(project)



    db.session.commit()
