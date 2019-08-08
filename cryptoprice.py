import requests


def get_crypto_price(code):
    url = f"https://api.cryptonator.com/api/ticker/{code}-eur"
    result = requests.request("GET", url)
    data = result.json()
    if ("ticker" in data) and ("price" in data["ticker"]):
        return data["ticker"]["price"]
    else:
        return -1


def get_crypto_change(code):
    url = f"https://api.cryptonator.com/api/ticker/{code}-eur"
    result = requests.request("GET", url)
    data = result.json()
    if ("ticker" in data) and ("change" in data["ticker"]):
        return data["ticker"]["change"]
    else:
        return -1


if __name__ == '__main__':
    for crypto_code in ["btc", "eth", "xrp", "bch", "ltc", "bnb", "eos", "bsv", "xmr", "xlm"]:
        price = get_crypto_price(crypto_code)
        change = get_crypto_change(crypto_code)
        print(crypto_code, price, change)

    for newcrypto_code in []:
        price = get_crypto_price(crypto_code)
        change = get_crypto_change(crypto_code)
        print(crypto_code, price, change)