
from flask import Blueprint, render_template

from .models import Goods

goods_blue = Blueprint('goods_blue', __name__)

@goods_blue.route('/')
def index():
    # return f'Hello, 我是商品页面！'
    return render_template('goods/index.html')