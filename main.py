from flask import Flask, url_for, redirect, render_template, request, make_response, Response, Request
import uuid
import hashlib
from datetime import time
from cryptoprice import get_crypto_price
from cryptoprice import get_crypto_change
from models import db, User, Cryptocurrency

app = Flask(__name__)

db.create_all()


def load_dummies():
    btc = Cryptocurrency(
        id=1,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/1.png",
        code="BTC",
        name="Bitcoin",
        price=200,
        change=1
    )

    eth = Cryptocurrency(
        id=2,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/1027.png",
        code="ETH",
        name="Ethereum",
        price=200,
        change=1
    )

    xrp = Cryptocurrency(
        id=3,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/52.png",
        code="XRP",
        name="XRP",
        price=200,
        change=1
    )

    bch = Cryptocurrency(
        id=4,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/1831.png",
        code="BCH",
        name="Bitcoin Cash",
        price=200,
        change=1
    )

    ltc = Cryptocurrency(
        id=5,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/2.png",
        code="LTC",
        name="Litecoin",
        price=200,
        change=1
    )

    bnb = Cryptocurrency(
        id=6,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/1839.png",
        code="BNC",
        name="Binance Coin",
        price=200,
        change=1
    )

    usdt = Cryptocurrency(
        id=7,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/825.png",
        code="USDT",
        name="Tether",
        price=200,
        change=1
    )

    eos = Cryptocurrency(
        id=8,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/1765.png",
        code="EOS",
        name="EOS",
        price=200,
        change=1
    )

    bsv = Cryptocurrency(
        id=9,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/3602.png",
        code="BSV",
        name="Bitcoin SV",
        price=200,
        change=1
    )

    xmr = Cryptocurrency(
        id=10,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/328.png",
        code="XMR",
        name="Monero",
        price=200,
        change=1
    )

    cryptocurrencies = [btc, eth, xrp, bch, ltc, bnb, usdt, eos, bsv, xmr]

    for crypto in cryptocurrencies:
        db_crypto = db.query(Cryptocurrency).filter_by(code=crypto.code).first()
        if db_crypto:
            print("Skipping", crypto.code)
            continue
        else:
            print("Saving", crypto.code)
            db.add(crypto)
            db.commit()


load_dummies()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.route("/newsletter")
def newsletter():
    return render_template("newsletter.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
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

            response: Response = make_response(redirect(url_for('cryptoverse')))
            response.set_cookie("session_cookie", session_cookie, expires=time.time() + 3600)
            return response

        return redirect(url_for("login"))


@app.route("/cryptoverse", methods=["GET", "POST"])
def cryptoverse():
    if request.method == "GET":
        cryptocurrencies = db.query(Cryptocurrency).all()
        for crypto in cryptocurrencies:
            crypto.price = get_crypto_price(crypto.code)
            crypto.change = get_crypto_change(crypto.code)
        db.add_all(cryptocurrencies)
        db.commit()

        return render_template("cryptoverse.html",
                               cryptocurrencies=cryptocurrencies,
                               showAll=True)
    elif request.method == "POST":
        crypto = Cryptocurrency(
            id=request.form.get("id"),
            imgLink=request.form.get("imgLink"),
            name=request.form.get("name"),
            code=request.form.get("code"),
            price=float(request.form.get("price")),
            change=float(request.form.get("change")),
        )
        db.add(crypto)
        db.commit()
        return redirect(url_for('cryptoverse'))


@app.route("/portfolio/<crypto_code>/add", methods=["GET", "POST"])
def crypto_edit(crypto_code):
    if request.method == "GET":
        crypto = db.query(Cryptocurrency).filter_by(code=crypto_code).first()
        return render_template("portfolio.html",
                               currentCrypto=crypto,
                               showAll=False)
    elif request.method == "POST":
        crypto = db.query(Cryptocurrency).filter_by(code=crypto_code).first()
        crypto.id = request.form.get("id")
        crypto.imgLink = request.form.get("imgLink")
        crypto.name = request.form.get("name")
        crypto.code = request.form.get("code")
        crypto.price = float(request.form.get("price"))
        crypto.change = float(request.form.get("change"))
        db.add(crypto)
        db.commit()
        return redirect(url_for("portfolio"))


@app.route("/portfolio/<crypto_code>/delete", methods=["GET"])
def crypto_delete(crypto_code):
    crypto = db.query(Cryptocurrency).filter_by(code=crypto_code).first()
    db.delete(crypto)
    db.commit()
    return redirect(url_for("portfolio"))


if __name__ == '__main__':
    app.run()
