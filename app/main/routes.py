from re import split
from flask import render_template, request, redirect, url_for, session
from sqlalchemy import asc, desc
from app import socketio
from app.auth import check_user_type
from app.auth.routes import login_required, current_user
from app.main import main
from app.database import query_data, db
# from app.models.Rooms import Rooms
from app.models.News import Post
from app.main.forms import ArticleForm, ContactForm
from app.models.Contact import CompanyInfo
from datetime import datetime
from uuid import uuid4
import json
from app.models.User import Client, Author, Technician, Consultant, Manager, Admin

import os
import base64
from flask_socketio import emit, send, join_room, leave_room

import random
from string import ascii_lowercase, ascii_uppercase


@main.route('/')
def home():

    return render_template('main/home.html', news=Post.query.order_by(desc(Post.postid)).limit(4))


@main.route('/services')
def services():
    return render_template('main/services.html')


@main.route('/news', methods=['GET', 'POST'])
def news():
    query = query_data(Post)
    postid = request.args.get('postid')
    addPost = request.args.get('addpost')
    deletePost = request.args.get('deletepost')
    status_message = None

    # TODO: Pagination
    # POSTS_PER_PAGE = 5
    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page, POSTS_PER_PAGE, False)
    # next_url = url_for('main.news', page=posts.next_num) if posts.has_next else None
    # prev_url = url_for('main.news', page=posts.prev_num) if posts.has_prev else None
    # return render_template('main/news.html', posts=posts.items, next_url=next_url, prev_url=prev_url)

    # View article
    if postid is not None:
        form = ArticleForm()
        query = query_data(Post, filter_by={'postid': postid}, all=False)
        if query is not None:
            return render_template('main/article.html', article=query, form=form, status_message=status_message)

    # Admin and Author only
    if current_user.is_authenticated and (current_user.type == 'admin' or current_user.type == 'author'):

        # Edit article
        if postid is not None and current_user.is_authenticated:
            form = ArticleForm()
            if current_user.is_authenticated and (current_user.type == 'admin' or current_user.type == 'author'):
                if request.method == 'POST':
                    if form.validate_on_submit():
                        print(form.content.data)
                        try:
                            post = Post.query.filter_by(postid=postid).first()
                            post.image_name = form.image_view_onNews.data
                            post.title = form.title.data
                            post.content = form.content.data

                            db.session.add(post)
                            db.session.commit()
                            status_message = "Article updated successfully!"
                        except Exception as e:
                            print(f"Error occurred: {e}")
                            db.session.rollback()
                            status_message = "Failed to update article! Contact Administrator."

        query = query_data(Post, filter_by={'postid': postid}, all=False)
        if query is not None:
            return render_template('main/article.html', article=query, form=form, status_message=status_message)

        # Delete article
        if deletePost is not None:
            try:
                post = Post.query.filter_by(postid=deletePost).first()
                db.session.delete(post)
                db.session.commit()
                return redirect(url_for('main.news'))
            except Exception as e:
                print(f"Error occurred: {e}")
                db.session.rollback()

        # Add article
        if addPost is not None:
            try:
                latestPostID = max(
                    Post.query.all(), key=lambda x: x.postid).postid

                newPost = Post(title="Title",
                               content="Content",
                               date=datetime.utcnow(),
                               author=current_user.username,
                               image_name="Upload an image",
                               postid=latestPostID+1)
                db.session.add(newPost)
                db.session.commit()
                return redirect(url_for('main.news', postid=latestPostID+1))
            except Exception as e:
                print(f"Error occurred: {e}")
                db.session.rollback()

        # Set Featured News
        getRequest_for_featured_post = request.form.get(
            'select-featured-post')
        if getRequest_for_featured_post is not None:
            try:
                try:
                    exist_featured_post = Post.query.filter_by(
                        featured_post=True).all()
                    for post in exist_featured_post:
                        post.featured_post = False
                        db.session.add(post)
                        db.session.commit()
                        print(post.featured_post)
                except Exception as e:
                    print(f"Error occurred: {e}")
                    db.session.rollback()

                post = Post.query.filter_by(
                    postid=getRequest_for_featured_post).first()
                post.featured_post = True
                db.session.add(post)
                db.session.commit()
                status_message = "Featured post updated successfully!"
            except Exception as e:
                status_message = "Failed to update featured post! Contact Administrator."
                print(f"Error occurred: {e}")
                db.session.rollback()

    query = query_data(Post, all=True)
    first_exist_featured_post = Post.query.filter_by(
        featured_post=True).first()

    if first_exist_featured_post is None:
        featured_postid = 2
    else:
        featured_postid = first_exist_featured_post.postid

    return render_template('main/news.html', data=query, setFeaturedNews=featured_postid)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    error_message = ""
    form = ContactForm()
    if form.validate_on_submit():
        try:
            contact = CompanyInfo(employee_name=form.employee_name.data, company_name=form.company_name.data,
                                  company_email=form.company_email.data, industry=form.industry.data, company_size=form.company_size.data)
            db.session.add(contact)
            db.session.commit()
            error_message = "Thank you for your enquiry. We will get back to you as soon as possible."

        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()
            error_message = "Failed to send enquiry. Please try again later."

        print(error_message)

    return render_template('main/contact.html', form=form, error_message=error_message)


# def generate_unique_code(length):
#     while True:
#         code = ""
#         for _ in range(length):
#             code += random.choice(ascii_uppercase)

#         if code not in rooms:
#             break

#     return code


# rooms = {}


# @main.route('/contact/room', methods=["GET", "POST"])
# @login_required
# def room():

#     username = current_user.username
#     UserList = {'client': Client, 'author': Author,
#                 'technician': Technician, 'consultant': Consultant,
#                 'manager': Manager, 'admin': Admin}

#     user = (query_data(Client, filter_by={'username': username}, all=False) or
#             query_data(Author, filter_by={'username': username}, all=False) or
#             query_data(Technician, filter_by={'username': username}, all=False) or
#             query_data(Consultant, filter_by={'username': username}, all=False) or
#             query_data(Manager, filter_by={'username': username}, all=False) or
#             query_data(Admin, filter_by={'username': username}, all=False))

#     session.pop('staffName', None)
#     if request.method == "POST":
#         name = username
#         code = request.form.get("code")
#         join = bool(request.form.get("join", False))
#         create = bool(request.form.get("create", False))

#         randomRoomCode = generate_unique_code(4)

#         if not name:
#             return render_template("main/room/room.html", error="Please enter a name.", code=code, name=name)

#         if join and not code:
#             return render_template("main/room/room.html", error="Please enter a room code.", code=code, name=name)

#         roomids = (room.userids for room in Rooms.query.all())

#         # check if user is already in a room
#         for i in roomids:
#             if user.user_id in i:
#                 query = Rooms.query.filter(
#                     Rooms.userids.contains(user.user_id)).first()
#                 return redirect(url_for("main.chat", code=query.room_code))

#         if create == True:

#             # query = Rooms.query.filter(
#             #     Rooms.userids.contains(current_user.user_id)).first()
#             # if query is not None:
#             #     try:
#             #         db.session.delete(query)
#             #         db.session.commit()
#             #     except Exception as e:
#             #         print(f"Error occurred: {e}")
#             #         db.session.rollback()

#             try:
#                 createRoom = Rooms(userids=json.dumps(
#                     [user.user_id]), room_code=randomRoomCode)
#                 db.session.add(createRoom)
#                 db.session.commit()
#                 print("Room created successfully!")

#                 return redirect(url_for("main.chat", code=randomRoomCode))

#             except Exception as e:
#                 print(f"Error occurred: {e}")
#                 db.session.rollback()
#                 print("Failed to create room. Please try again later.")

#         # elif code not in room_code:
#         #     return render_template("main/room/room.html", error="Room does not exist.", code=code, name=name)

#         session['staffName'] = name

#         return redirect(url_for("main.room"))

#     query = Rooms.query.all()

#     return render_template("main/room/room.html", rooms=query)


# @main.route('/contact/room/chat', methods=["GET", "POST"])
# @login_required
# def chat():
#     username = current_user.username

#     session.pop('customerName', None)
#     getRoomCode = request.args.get("code")

#     session['roomCode'] = getRoomCode
#     session['customerName'] = username

#     name = session.get("customerName")

#     if getRoomCode is None or name is None:
#         return redirect(url_for("main.room"))

#     query = Rooms.query.filter_by(room_code=getRoomCode).first()
#     return render_template("main/room/chat.html", code=getRoomCode)


# for article image upload function
image_chunks = []


@socketio.on("upload_image")
def handle_upload(data):
    global image_chunks
    # Add the received chunk to the array
    image_chunks.append((data['index'], data['image']))

    # If this is the final chunk, concatenate all chunks to form the complete image
    if data['final']:
        image_chunks.sort(key=lambda x: x[0])  # Sort the chunks by index
        complete_image = ''.join(chunk[1] for chunk in image_chunks)
        image_chunks = []  # Clear the array for the next image

        # process the complete image
        prefix, base64_data = complete_image.split(",", 1)
        binary_data = base64.b64decode(base64_data)

        # generate string for filename
        filename = "upload-"
        for i in range(10):
            filename += random.choice(ascii_lowercase)

        # check file extension
        extention = ""
        if prefix == "data:image/jpeg;base64":
            extention = ".jpg"
        elif prefix == "data:image/png;base64":
            extention = ".png"
        elif prefix == "data:image/webp;base64":
            extention = ".webp"
        else:
            extention = ".jpg"

        # save image to file
        filename_path = os.path.join(
            './app/static/images/uploads', f'{filename}{extention}')

        print(filename)

        # write the binary data to a file
        with open(filename_path, 'wb') as f:
            f.write(binary_data)

        # Emit a response to the client
        emit('image_response', {
             'message': 'Image received', 'image': complete_image, "image_name": filename+extention}, broadcast=True)

# end of image upload function


# chat room function

# @socketio.on("message")
# def message(data):
#     roomCode = str(data['code'])
#     content = {
#         "staffName": session.get("staffName"),
#         "customerName": session.get("customerName"),
#         "message": data["data"]
#     }

#     session['roomCode'] = roomCode
#     send(content, to=roomCode)
#     try:
#         query = Rooms.query.filter_by(room_code=roomCode).first()

#         if query.messages is None:
#             query.messages = []

#         query.messages = json.dumps(json.loads(str(query.messages)) +
#                                     [content["message"]])
#         db.session.commit()
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         db.session.rollback()
#     # print(f"{session.get('name')} said: {data['data']}")


# @socketio.on("requestRoom")
# def connect(auth):
#     room = session.get("roomCode")
#     name = session.get("customerName")
#     print(room, name)
#     if not room or not name:
#         return

#     if room not in room:
#         leave_room(room)
#         return

#     content = {
#         'staffName': session.get("staffName"),
#         "customerName": name,
#         "message": "has entered the room"
#     }

#     join_room(room)
#     send(content, to=room)

#     # rooms[room]["members"] += 1
#     # print(f"{name} joined room {room}")


# @socketio.on("userDisconnected")
# def disconnect():
#     room = session.get("roomCode")
#     name = session.get("customerName")
#     leave_room(room)

#     # if room in rooms:
#     #     rooms[room]["members"] -= 1
#     #     if rooms[room]["members"] <= 0:
#     #         del rooms[room]

#     content = {
#         'staffName': session.get("staffName"),
#         "customerName": name,
#         "message": "has left the room"
#     }

#     send(content, to=room)
#     # print(f"{name} has left the room {room}")

# # end of chat room function
