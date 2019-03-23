
class Order(object):
	def __init__(self, dex_name, bid,  ask, volume, eth_price, price, fee):
		self.dex_name = dex_name
		self.bid_name = bid
		self.ask_name = ask
		self.volume = volume
		self.eth_price = eth_price
		self.price = price
		self.fee = fee
