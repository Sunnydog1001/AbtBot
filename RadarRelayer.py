import urllib.request
import json


pairs_url = "https://api.radarrelay.com/v2/markets"
book_url1 = "https://api.radarrelay.com/v2/markets/"
book_url2 = "/book"


class Order(object):
	def __init__(self, from_token = "",  to_token = "", from_amount = 0, eth_from_price = 0,
		eq_from_price = 0):
		self.from_token = from_token
		self.from_amount = from_amount
		self.eth_from_price = eth_from_price
		self.eq_from_price = eq_from_price
		self.to_token = to_token
		self.fee = 0

pairs = {}
orders = []
with urllib.request.urlopen(pairs_url) as response:
	jsn = response.read()
	markets = json.loads(jsn)
	for market in markets:
		pair = market["id"].split("-")
		pairs[pair[0]] = pair[1]
for pair in pairs:
	print(pair + "-" + pairs[pair])
	with urllib.request.urlopen(book_url1 + pair + "-" + pairs[pair] + book_url2) as response:
		jsn = response.read()
		info = json.loads(jsn)
		from_token = pair
		to_token = pairs[pair]
		bids = info["bids"]
		for bid in bids:
			from_amount = bid["remainingBaseTokenAmount"]
			eth_from_price = bid["price"]
			eq_from_price = eth_from_price
			order = Order(from_token, to_token, from_amount, eth_from_price, eq_from_price)
			orders.append(order)
print(orders)






