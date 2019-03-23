import urllib.request
import json
from order import Order


pairs_url = "https://api.radarrelay.com/v2/markets/"
book_url1 = "https://api.radarrelay.com/v2/markets/"
book_url2 = "/book"


def getBids(orders, market):
	try:
		with urllib.request.urlopen(book_url1 + market + book_url2) as response:
			jsn = response.read()
			info = json.loads(jsn)
			pair = market.split("-")
			from_token = pair[0]
			to_token = pair[1]
			bids = info["bids"]
			for bid in bids:
				from_amount = bid["remainingBaseTokenAmount"]
				eth_from_price = bid["price"]
				eq_from_price = eth_from_price
				order = Order(from_token, to_token, from_amount, eth_from_price, eq_from_price)
				orders.append(order)
	except:
		print("error")

def getAsks(orders, market):
	try:
		with urllib.request.urlopen(book_url1 + market + book_url2) as response:
			jsn = response.read()
			info = json.loads(jsn)
			pair = market.split("-")
			from_token = pair[1]
			to_token = pair[0]
			asks = info["asks"]
			for ask in asks:
				from_amount = ask["remainingBaseTokenAmount"]
				eth_from_price = ask["price"]
				eq_from_price = eth_from_price
				order = Order(from_token, to_token, from_amount, eth_from_price, eq_from_price)
				orders.append(order)
	except:
		print("error")


def
pairs = {}
orders = []
with urllib.request.urlopen(pairs_url) as response:
	jsn = response.read()
	markets = json.loads(jsn)
	for market in markets:
		pair = market["id"]
		getBids(orders, pair)
		getAsks(orders, pair)

for order in orders:
	print(order.bid_name, order.ask_name, order.volume, order.price)






