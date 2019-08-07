from flask import Flask, url_for, redirect, render_template, request, make_response, Response, Request
import datetime
import random
import uuid
import hashlib
from read_crypto_api import get_crypto_price
from models import db, User, CryptoCurrency

app = Flask(__name__)

db.create_all()

def load_dummies()







@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        email = request.form.get("email")
        password = hashlib.sha256(request.form.get("password").encode("utf-8")).hexdigest()

        logged_in = False

        user = db.query(User).filter_by(email=email).first()

        if not user:
            user = User(email=email, password=password)
            db.add(user)
            db.commit()

        if password == user.password:
            session_cookie = str(uuid.uuid4())

            user.session_token = session_cookie
            db.add(user)
            db.commit()

            response: Response = make_response(redirect(url_for('index')))
            response.set_cookie("session_cookie", session_cookie, expires=time.time() + 3600)
            return response

            # render_template
            # -> show html now on this url where you are

            # redirect
            # -> move to new url, make get request there
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()