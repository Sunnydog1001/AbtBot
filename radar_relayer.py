import urllib.request
import json
from order import Order
from orderbook import Orderbook

pairs_url = "https://api.radarrelay.com/v2/markets/"
book_url1 = "https://api.radarrelay.com/v2/markets/"
book_url2 = "/book"

def get_bids(orderbook : Orderbook, market):
	try:
		with urllib.request.urlopen(book_url1 + market + book_url2) as response:
			jsn = response.read()
			info = json.loads(jsn)
			pair = market.split("-")
			from_token = pair[0]
			to_token = pair[1]
			bids = info["bids"]

			print("Downloading data...")

			for bid in bids:
				from_amount = bid["remainingBaseTokenAmount"]
				eth_from_price = bid["price"]
				eq_from_price = eth_from_price
				order = Order("Radar Relayer", from_token, to_token,
                              float(from_amount), float(eth_from_price), float(eq_from_price), 0)
				orderbook.add_order(order)
	except:
		print("error")

def get_asks(orderbook, market):
	try:
		with urllib.request.urlopen(book_url1 + market + book_url2) as response:
			jsn = response.read()
			info = json.loads(jsn)
			pair = market.split("-")
			from_token = pair[1]
			to_token = pair[0]
			asks = info["asks"]

			print("Downloading data...")

			for ask in asks:
				from_amount = ask["remainingBaseTokenAmount"]
				eth_from_price = ask["price"]
				eq_from_price = eth_from_price
				order = Order("Radar Relayer", from_token, to_token,
                              float(from_amount), float(eth_from_price), float(eq_from_price), 0)

				orderbook.add_order(order)
	except:
		print("error")


def get_info(orderbook):

	with urllib.request.urlopen(pairs_url) as response:
		jsn = response.read()
		markets = json.loads(jsn)
		for market in markets:
			pair = market["id"]
			get_bids(orderbook, pair)
			get_asks(orderbook, pair)
