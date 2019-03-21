import urllib.request
import json

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
	with urllib.request.urlopen(token_data_url1 + token + token_data_url2) as response:
		jsn = response.read()
		info = json.loads(jsn)
		info = info["data"]["page"][0]
	return info["_id"]


def getAmount(token1, token2):
	with urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + token2) as response:
		jsn = response.read()
		info = json.loads(jsn)
		info = info["data"]
	return info["totalSupplyD"]

def getPriceEth(tokenq, token2):
	with urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + "ETH") as response:
		jsn = response.read()
		info = json.loads(jsn)
		info = info["data"]
	return info["price24h"]

def getPriceEq(tokenq, token2):
	with urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + token2) as response:
		jsn = response.read()
		info = json.loads(jsn)
		info = info["data"]
	return info["price24h"]

class Order(object):
	def __init__(self, from_token = "",  to_token = "", from_amount = 0, eth_from_price = 0,
		eq_from_price = 0):
		self.from_token = from_token
		self.from_amount = from_amount
		self.eth_from_price = eth_from_price
		self.eq_from_price = eq_from_price
		self.to_token = to_token


order_list = []

with urllib.request.urlopen(availible_pairs_url) as response:
	jsn = response.read()
	availible_pairs = json.loads(jsn);
	availible_pairs = availible_pairs["data"] #пары доступных пар для обмена

for pair in availible_pairs:
	print (pair, availible_pairs[pair])
	token1 = pair
	token2 = availible_pairs[pair]
	token1_amount = getAmount(token1, token2)
	eth_price = getPriceEth(token1, token2)
	eq_price = getPriceEq(token1, token2)
	order = Order(token1, token2, token1_amount, eth_price, eq_price)
	order_list.append(order)



	
print(order_list)