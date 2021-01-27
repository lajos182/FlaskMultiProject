from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restful import Api
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from ..middlewares.custom_middleware import load_middleware

db = SQLAlchemy()
migrate = Migrate()
sess = Session()
cache = Cache(config={
    'CACHE_TYPE': 'redis'
})
mail = Mail()

def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    sess.init_app(app)
    Bootstrap(app)
    # DebugToolbarExtension(app)
    cache.init_app(app)
    load_middleware(app)
    mail.init_app(app)
