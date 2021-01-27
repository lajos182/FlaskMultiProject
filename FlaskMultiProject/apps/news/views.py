import base64
import os
import random
import time

from flask import Blueprint, render_template, request, g, current_app

from .models import News
from ..extensions import db
from ...settings import BASE_DIR
from ...utils.data_secret import make_data_secret

news_blue = Blueprint('news_blue', __name__)

@news_blue.route('/')
def index():
    return 'News Index'

@news_blue.route('/addnews/')
def add_news():
    new = News()
    new.title = f'郑爽{random.randrange(1000)}'
    new.content = f'代孕事件, 豪宅, ... {random.randrange(10000)}'
    db.session.add(new)
    db.session.commit()
    return 'Add News Success'

@news_blue.route('/getnews/')
def get_news():
    news = News.query.all()
    news_content = render_template('news/news_content.html', news=news)
    encode_content_twice = make_data_secret(news_content)
    return render_template('news/news_list.html', news_content=news_content, encode_content_twice=encode_content_twice)

@news_blue.route('/getshowjs/')
def get_show_js():
    t = request.args.get('t', type=int, default=0)
    c = int(1000 * time.time())
    if c > t and c - t < 1000:
        with open(os.path.join(BASE_DIR, 'FlaskMultiProject/static/js/show.js'), 'r') as fp:
            js_content = fp.read()
        return js_content
    else:
        return f'1{g.msg}'

@news_blue.before_request
def before():
    print(request.url)
    g.msg = '呵呵哒'
    config = current_app.config
    print(config, '------')
    keys = config.keys()
    for key in keys:
        print(key, config.get(key))

@news_blue.after_request
def after(resp):
    print('after')
    print(resp)
    print(type(resp))
    return resp