
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
