
from .user import user_blue
from .goods import goods_blue
from .index import index_blue

# 专门配置蓝本，减少代码的重复度
DEFAULT_BLUEPRINT = {
    # (蓝本, 前缀)
    (index_blue, ''),
    (user_blue, '/user'),
    (goods_blue, '/goods'),
}
def init_view(app):
    for blueprint, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint=blueprint, url_prefix=url_prefix)