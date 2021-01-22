from FlaskMultiProject.apps.extensions import db

class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    price = db.Column(db.String(16), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()