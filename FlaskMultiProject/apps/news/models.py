
from ..extensions import db

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32))
    content = db.Column(db.String(256))