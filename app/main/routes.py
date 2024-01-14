from re import S
from flask import render_template, request, redirect, url_for, session
from flask_login import current_user
from sqlalchemy import desc
from app import socketio
from app.main import main
from app.database import query_data, db
from app.models.News import Post
from app.main.forms import ArticleForm, ContactForm
from app.models.Contact import CompanyInfo

import os
import base64
from flask_socketio import emit, send, join_room, leave_room

import random
from string import ascii_lowercase, ascii_uppercase


@main.route('/')
def home():
    return render_template('main/home.html', news=query_data(Post, limit=3))


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
    if current_user.is_authenticated and (current_user.type == 'admin' or current_user.type == 'author'):
        if deletePost is not None:
            try:
                post = Post.query.filter_by(postid=deletePost).first()
                db.session.delete(post)
                db.session.commit()
                return redirect(url_for('main.news'))
            except Exception as e:
                print(f"Error occurred: {e}")
                db.session.rollback()

        if addPost is not None:
            latestPostID = Post.query.order_by(desc(Post.date)).first().postid
            try:
                newPost = Post(title="Title",
                               content="",
                               author=current_user.username,
                               image_name="Upload an image",
                               postid=latestPostID+1)
                db.session.add(newPost)
                db.session.commit()
                return redirect(url_for('main.news', postid=latestPostID+1))
            except Exception as e:
                print(f"Error occurred: {e}")
                db.session.rollback()

        getRequest_for_featured_post = request.form.get('select-featured-post')
        exist_featured_post = Post.query.filter_by(featured_post=True).all()
        if getRequest_for_featured_post is not None:
            try:
                try:
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

    if postid is not None:
        form = ArticleForm()
        if current_user.is_authenticated and (current_user.type == 'admin' or current_user.type == 'author'):
            if request.method == 'POST':
                if form.validate_on_submit():
                    if request.form.get('csrf_token'):
                        try:
                            post = Post.query.filter_by(postid=postid).first()
                            post.image_name = form.image_view_onNews.data
                            post.title = form.title.data
                            post.content = form.content.data

                            db.session.add(post)
                            db.session.commit()
                            status_message = "Article updated successfully!"
                        except Exception as e:
                            status_message = "Failed to update article! Contact Administrator."
                            print(f"Error occurred: {e}")
                            db.session.rollback()

        query = query_data(Post, filter_by={'postid': postid}, all=False)
        if query is not None:
            return render_template('main/article.html', article=query, form=form, status_message=status_message)

    first_exist_featured_post = Post.query.filter_by(
        featured_post=True).first()

    if first_exist_featured_post is None:
        featured_postid = 0
    else:
        featured_postid = first_exist_featured_post.postid

    return render_template('main/news.html', data=query, setFeaturedNews=featured_postid)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    error_message = None
    form = ContactForm()
    if form.validate_on_submit():
        try:
            contact = CompanyInfo(employee_name=form.employee_name.data, company_name=form.company_name.data,
                                  company_email=form.company_email.data, industry=form.industry.data, company_size=form.company_size.data)
            db.session.add(contact)
            db.session.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()

        error_message = "Thank you for your enquiry. We will get back to you as soon as possible."

    return render_template('main/contact.html', form=form, error_message=error_message)


def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code


rooms = {}


@main.route('/contact/room', methods=["GET", "POST"])
def room():
    session.pop("room", None)
    session.pop("name", None)
    if request.method == "POST":
        print("contact/room POST")
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("main/room/room.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("main/room/room.html", error="Please enter a room code.", code=code, name=name)

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("main/room/room.html", error="Room does not exist.", code=code, name=name)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("main.chat"))

    return render_template("main/room/room.html")


@main.route('/contact/room/chat', methods=["GET", "POST"])
def chat():
    print("room/chat")
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("main.room"))

    return render_template("main/room/chat.html", code=room, messages=rooms[room]["messages"])


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
            './app/static/images/', f'{filename}{extention}')

        print(filename)

        # write the binary data to a file
        with open(filename_path, 'wb') as f:
            f.write(binary_data)

        # Emit a response to the client
        emit('image_response', {
             'message': 'Image received', 'image': complete_image, "image_name": filename+extention}, broadcast=True)

# end of image upload function


# chat room function

@socketio.on("message")
def message(data):
    print("message", data)
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")


@socketio.on("requestRoom")
def connect(auth):
    print("connect", auth)
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")


@socketio.on("userDisconnected")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

# end of chat room function
