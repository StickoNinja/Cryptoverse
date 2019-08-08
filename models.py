import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(
    os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    session_token = db.Column(db.String)


class Cryptocurrency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imgLink = db.Column(db.String)
    code = db.Column(db.String, unique=True)
    name = db.Column(db.String, unique=True)
    price = db.Column(db.Float)
    change = db.Column(db.Float)
    quantity = db.Column(db.Integer)
