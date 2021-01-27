from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db

class User(db.Model):
    __tablename__ = 'UserModel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    description = db.Column(db.String(128), nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True)
    password_hash = db.Column(db.String(256), nullable=True)
    phone = db.Column(db.String(32), unique=True)

    @property
    def password(self):
        raise Exception("Error Action: Password can't be access")

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Animal(db.Model):
    __abstract__ = True  # 设置抽象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16))

class Dog(Animal):
    habit = db.Column(db.String(128), default='')

class Cat(Animal):
    eat = db.Column(db.String(128), default='fish')

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16))
    addresses = db.relationship('Address', backref='customer', lazy=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    position = db.Column(db.String(128))
    customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id))