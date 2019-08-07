import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(
    os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite")
)  # this connects to a database either on Heroku or on localhost


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    session_token = db.Column(db.String)


class CryptoCurrency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    imgLink = db.Column(db.String)
    ticker = db.Column(db.String, unique=True)
    name = db.Column(db.String, unique=True)
    price = db.Column(db.Float)
    marketCap = db.Column(db.Float)

