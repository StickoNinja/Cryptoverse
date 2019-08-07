import requests

def cryptoprice(code):
    url = f"https://api.cryptonator.com/api/ticker/{code}-eur"
    result = requests.request("GET", url)
    data = result.json()
    if ("ticker" in data) and ("price" in data["ticker"]):
        return data["ticker"]["price"]
    else:
        return -1


if __name__ == '__main__':
    for cryptoticker in ["btc", "eth", "qnt"]:
        price = cryptoprice(cryptoticker)
        print(cryptoticker, price)