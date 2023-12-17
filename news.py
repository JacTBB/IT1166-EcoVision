import datetime
import shelve


class Post:
    def __init__(self, postid, date, image, title, description):
        self.postid = postid
        self.date = datetime.datetime.strptime(date, "%d %m %Y").date()
        self.image = image
        self.title = title
        self.description = description


# sample data
postid = 1
with shelve.open("news") as data:
    for i in range(1, 5):
        data[str(postid)] = Post(postid, "20 10 2023",
                                 "Cover-image-1-495x400.jpg",  "TEstESt", "Lorem ipsum dolor sit amet consectetur adipisicing elit. Aut, iure eos aspernatur autem dicta minima et commodi? Quia tempora voluptatibus fugit labore dolor reiciendis facilis. Nam eligendi deserunt minus unde?")
        postid += 1

# read database
# try:
#     with shelve.open("news") as data:
#         for k, v in sorted(data.items()):
#             print(v.postid, v.date, v.description, v.image, v.title)

# except IOError:
#     print("Error: can\'t find file or read data")


# while True:
#     try:
#         inputDate = input("Enter date in format 'DD MM YYYY': ")
#         if inputDate == "exit":
#             break
#         inputDescription = input("Enter description: ")

#         with shelve.open("news") as data:
#             post_id = len(data) + 1
#             h = data[str(post_id)] = Post(post_id, inputDate, inputDescription)
#             print("Post added")
#             print(h.postid, h.date, h.description)
#     except ValueError:
#         print("Incorrect data format, should be DD MM YYYY")
