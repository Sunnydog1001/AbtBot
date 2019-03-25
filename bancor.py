import urllib.request
import json
from order import Order

bancor_url = "https://api.bancor.network/0.1/currencies/"
availible_pairs_url = "https://api.bancor.network/0.1/currencies/convertiblePairs"
token_info_url = "https://api.bancor.network/0.1/converters?code="
exchange_url1 = "https://api.bancor.network/0.1/currencies/"
exchange_url2 = "/value?toCurrencyId="
exchange_url3 = "&toAmount=1000000000000000000"

token_data_url1 = "https://api.bancor.network/0.1/currencies/tokens?limit=1&skip=0&fromCurrencyCode="
token_data_url2 = "&includeTotal=false&orderBy=price&sortOrder=desc"
tiker1 = "https://api.bancor.network/0.1/currencies/"
tiker2 = "/ticker?fromCurrencyCode="
tiker3 = "&displayCurrencyCode="

def getId(token):
    try:
        with urllib.request.urlopen(token_data_url1 + token + token_data_url2) as response:
            jsn = response.read()
            info = json.loads(jsn)
            info = info["data"]["page"][0]
        return info["_id"]
    except Exception as exc:
        print(exc)


def getAmount(token1, token2):
    try:
        with urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + token2) as response:
            jsn = response.read()
            info = json.loads(jsn)
            info = info["data"]
        return info["totalSupplyD"]
    except Exception as exc:
        print(exc)


def getPriceEth(token1, token2):
    try:
        urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + "ETH")

        with urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + "ETH") as response:
            jsn = response.read()
            info = json.loads(jsn)
            info = info["data"]

        return info["price24h"]
    except Exception as exc:
        print(exc)


def getPriceEq(token1, token2):
    try:
        with urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + token2) as response:
            jsn = response.read()
            info = json.loads(jsn)
            info = info["data"]
        return info["price24h"]
    except Exception as exc:
        print(exc)


def getPriceEq_and_Amount(token1, token2):
    try:
        with urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + token2) as response:
            jsn = response.read()
            info = json.loads(jsn)
            info = info["data"]
            return info["price24h"], info["totalSupplyD"]
    except Exception as exc:
        print(exc)


def make_order(token1, token2):
    price_and_amount = getPriceEq_and_Amount(token1, token2)
    eth_price = getPriceEth(token1, token2)
    if price_and_amount[1] == -1 or eth_price == -1 or price_and_amount[0] == -1:
        return -1

    order = Order("Bancor", token1, token2, price_and_amount[1], eth_price, price_and_amount[0], 0)
    return order


def get_info(orderbook):
    try:
        with urllib.request.urlopen(availible_pairs_url) as response:
            jsn = response.read()
            availible_pairs = json.loads(jsn)
            availible_pairs = availible_pairs["data"]

        for token in availible_pairs:
            order = make_order(token, availible_pairs[token])
            if (order == -1):
                continue

            orderbook.add_order(order)

            order = make_order(availible_pairs[token], token)
            if (order == -1):
                continue

            orderbook.add_order(order)

    except Exception as exc:
        print(exc)
