from flask import render_template, request
from app.main import main
from app.database import query_data
from app.models.News import Post
from app.main.forms import ArticleForm



@main.route('/')
def home():
    return render_template('main/home.html', news=query_data(Post, limit=3))



@main.route('/services')
def services():
    return render_template('main/services.html')



@main.route('/news')
def news():
    query = query_data(Post)
    postid = request.args.get('postid')
    if postid is not None:
        form = ArticleForm()
        query = query_data(Post, filter_by={'postid': postid}, all=False)
        if query is not None:
            return render_template('main/article.html', article=query, form=form)

    return render_template('main/news.html', data=query)