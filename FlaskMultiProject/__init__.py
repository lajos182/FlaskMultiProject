
from flask import Flask

from .apps.applications import init_view
from .apps.extensions import init_ext
from .settings import envs


def create_app(env):
    app = Flask(__name__)
    # 加载settings中的配置
    app.config.from_object(envs.get(env))
    # 加载扩展库
    init_ext(app)
    # 加载路由
    init_view(app)
    return app