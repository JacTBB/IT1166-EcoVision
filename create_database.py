import datetime
import shelve


class Post:
    def __init__(self, image, title, content, author, date, postid):
        self.postid = postid
        self.date = datetime.datetime.strptime(
            date, "%d %m %Y").date().strftime("%B %d, %Y")
        self.image = image
        self.title = title
        self.content = content
        self.author = author


# sample data
postid = 1
with shelve.open("news") as data:
    for i in range(1, 3):
        data[str(postid)] = Post("Cover-image-1-495x400.jpg", "Title",
                                 "Lorem ipsum dolor sit amet consectetur Lorem ipsum dolor sit amet consectetur", "Author", "20 11 2023", postid)
        postid += 1

    postid = 3
    for i in range(3, 7):
        data[str(postid)] = Post("Cover-image-1-495x400.jpg", "Title",
                                 "Lorem ipsum dolor sit amet consectetur adipisicing elit. Aut, <b>iure eos aspernatur autem dicta minima et commodi?</b> Quia tempora voluptatibus fugit labore dolor reiciendis facilis. Nam eligendi deserunt minus unde?", "Author", "20 10 2023", postid)
        postid += 1


# read database
# try:
#     with shelve.open("news") as data:
#         for k, v in sorted(data.items()):
#             print(v.postid, v.date, v.description, v.image, v.title)

# except IOError:
#     print("Error: can\'t find file or read data")
