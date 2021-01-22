
from ..extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()