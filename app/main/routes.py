from flask import render_template, request, redirect, url_for
from flask_login import login_remembered, login_required
from app.main import main
from app.database import query_data, db
from app.models.News import Post
from app.main.forms import ArticleForm


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
    if postid is not None:
        form = ArticleForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                if request.form.get('csrf_token'):
                    try:
                        post = Post.query.filter_by(postid=postid).first()
                        post.title = form.title.data
                        post.content = form.content.data

                        db.session.add(post)
                        db.session.commit()
                    except Exception as e:
                        print(f"Error occurred: {e}")
                        db.session.rollback()

        query = query_data(Post, filter_by={'postid': postid}, all=False)
        if query is not None:
            return render_template('main/article.html', article=query, form=form)

    return render_template('main/news.html', data=query)
