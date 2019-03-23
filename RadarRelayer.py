import urllib.request
import json


pairs_url = "https://api.radarrelay.com/v2/markets/"
book_url1 = "https://api.radarrelay.com/v2/markets/"
book_url2 = "/book"


class Order(object):
	def __init__(self, bid = "",  ask = "", volume = 0, eth_price = 0,
		price = 0):
		self.dex_name = "RadarRelayer"
		self.bid_name = bid
		self.ask_name = ask
		self.volume = volume
		self.eth_price = eth_price
		self.price = price
		self.fee = 0

def getBids(orders, market):
	try:
		urllib.request.urlopen(book_url1 + market + book_url2)
	except:
		return
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

def getAsks(orders, market):
	try:
		urllib.request.urlopen(book_url1 + market + book_url2)
	except:
		return
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

pairs = {}
orders = []
with urllib.request.urlopen(pairs_url) as response:
	jsn = response.read()
	markets = json.loads(jsn)
	for market in markets:
		pair = market["id"]
		getBids(orders, pair)
		getAsks(orders, pair)
print(len(orders))






