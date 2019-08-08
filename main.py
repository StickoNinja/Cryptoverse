from flask import Flask, url_for, redirect, render_template, request, make_response, Response, Request
import uuid
import hashlib
from datetime import time
from cryptoprice import get_crypto_price
from cryptoprice import get_crypto_change
from models import db, User, Cryptocurrency, Newcrypto

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
        code="BNB",
        name="Binance Coin",
        price=200,
        change=1
    )

    eos = Cryptocurrency(
        id=7,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/1765.png",
        code="EOS",
        name="EOS",
        price=200,
        change=1
    )

    bsv = Cryptocurrency(
        id=8,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/3602.png",
        code="BSV",
        name="Bitcoin SV",
        price=200,
        change=1
    )

    xmr = Cryptocurrency(
        id=9,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/328.png",
        code="XMR",
        name="Monero",
        price=200,
        change=1
    )

    xlm = Cryptocurrency(
        id=10,
        imgLink="https://s2.coinmarketcap.com/static/img/coins/32x32/825.png",
        code="XLM",
        name="Stellar",
        price=200,
        change=1
    )

    qnt = Newcrypto(
        code="QNT",
        name="Quantnetwork",
        price=200,
        quantity=50
    )

    cryptocurrencies = [btc, eth, xrp, bch, ltc, bnb, eos, bsv, xmr, xlm]

    for crypto in cryptocurrencies:
        db_crypto = db.query(Cryptocurrency).filter_by(code=crypto.code).first()
        if db_crypto:
            print("Skipping", crypto.code)
            continue
        else:
            print("Saving", crypto.code)
            db.add(crypto)
            db.commit()

    newcryptos = [qnt]

    for newcrypto in newcryptos:
        db_newcrypto = db.query(Newcrypto).filter_by(code=newcrypto.code).first()
        if db_newcrypto:
            print("Skipping", newcrypto.code)
            continue
        else:
            print("Saving", newcrypto.code)
            db.add(newcrypto)
            db.commit()


load_dummies()


@app.route("/")
def index():
    return render_template("index.html")


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
            response.set_cookie("session_cookie", session_cookie)
            return response

        return redirect(url_for('cryptoverse'))


@app.route("/cryptoverse")
def cryptoverse():
        cryptocurrencies = db.query(Cryptocurrency).all()
        for crypto in cryptocurrencies:
            crypto.price = get_crypto_price(crypto.code)
            crypto.change = get_crypto_change(crypto.code)
        db.add_all(cryptocurrencies)
        db.commit()

        return render_template("cryptoverse.html",
                               cryptocurrencies=cryptocurrencies,
                               showAll=True)

        db.add(crypto)
        db.commit()
        return redirect(url_for('cryptoverse'))


@app.route("/portfolio", methods=["GET", "POST"])
def portfolio():
    if request.method == "GET":
        newcryptos = db.query(Newcrypto).all()
        for newcrypto in newcryptos:
            newcrypto.price = get_crypto_price(newcrypto.code)
        db.add_all(newcryptos)
        db.commit()

        return render_template("portfolio.html",
                               newcryptos=newcryptos,
                               showAll=True)
    elif request.method == "POST":
        newcrypto = Newcrypto(
            name=request.form.get("name"),
            code=request.form.get("code"),
            price=request.form.get("price"),
            quantity=request.form.get("quantity"),
        )

        db.add(newcrypto)
        db.commit()
        return redirect(url_for('portfolio'))


@app.route("/portfolio/<newcrypto_code>/edit", methods=["GET", "POST"])
def newcrypto_edit(newcrypto_code):
    if request.method == "GET":
        newcrypto = db.query(Newcrypto).filter_by(code=newcrypto_code).first()
        return render_template("portfolio.html",
                               currentCrypto=newcrypto,
                               showAll=False)
    elif request.method == "POST":
        newcrypto = db.query(Newcrypto).filter_by(code=newcrypto_code).first()
        newcrypto.name = request.form.get("name")
        newcrypto.code = request.form.get("code")
        newcrypto.price = float(request.form.get("price"))
        newcrypto.quantity = float(request.form.get("quantity"))
        db.add(newcrypto)
        db.commit()
        return redirect(url_for("portfolio"))


@app.route("/portfolio/<newcrypto_code>/delete", methods=["GET"])
def newcrypto_delete(newcrypto_code):
    newcrypto = db.query(Newcrypto).filter_by(code=newcrypto_code).first()

    db.delete(newcrypto)
    db.commit()
    return redirect(url_for("portfolio"))


if __name__ == '__main__':
    app.run()
