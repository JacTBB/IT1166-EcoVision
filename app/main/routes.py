from flask import render_template, request, redirect, url_for
from flask_login import current_user
from sqlalchemy import desc
from app.main import main
from app.database import query_data, db
from app.models.News import Post
from app.main.forms import ArticleForm, ContactForm
from app.models.Contact import CompanyInfo


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

    # employee_name: Mapped[str] = mapped_column(String)
    # company_name: Mapped[str] = mapped_column(String)
    # company_email: Mapped[str] = mapped_column(String)
    # industry: Mapped[str] = mapped_column(String)
    # company_size: Mapped[int] = mapped_column(Integer)


@main.route('/contact/chat')
def chat():
    return "hi"
