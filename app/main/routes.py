from flask import render_template, request, redirect, url_for, session
from flask_login import current_user
from sqlalchemy import desc
from app import socketio
from app.main import main
from app.database import query_data, db
from app.models.News import Post
from app.main.forms import ArticleForm, ContactForm
from app.models.Contact import CompanyInfo

from flask_socketio import send, join_room, leave_room

import random
from string import ascii_uppercase


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
                newPost = Post(title="blank",
                               content="blank",
                               author=current_user.username,
                               image_name="idk",
                               postid=latestPostID+1)
                db.session.add(newPost)
                db.session.commit()
                return redirect(url_for('main.news', postid=latestPostID+1))
            except Exception as e:
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

    return render_template('main/news.html', data=query)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
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

        return redirect(url_for('main.home'))

    return render_template('main/contact.html', form=form)


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


@socketio.on("connect")
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


@socketio.on("disconnect")
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
