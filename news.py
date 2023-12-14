


#sample data


import shelve

with shelve.open("news") as data:
    number = 1
    data["news"] = {
        "postid": 1,
        "Date": "12/1/2023",
        "description": "hello"
    }

