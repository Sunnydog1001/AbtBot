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
	try:
		urllib.request.urlopen(token_data_url1 + token + token_data_url2)
	except:
		return -1
	with urllib.request.urlopen(token_data_url1 + token + token_data_url2) as response:
		jsn = response.read()
		info = json.loads(jsn)
		info = info["data"]["page"][0]
	return info["_id"]


def getAmount(token1, token2):
	try:
		urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + token2)
	except:
		return -1
	with urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + token2) as response:
		jsn = response.read()
		info = json.loads(jsn)
		info = info["data"]
	return info["totalSupplyD"]

def getPriceEth(tokenq, token2):
	try:
		urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + "ETH")
	except:
		return -1
	with urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + "ETH") as response:
		jsn = response.read()
		info = json.loads(jsn)
		info = info["data"]
	return info["price24h"]

def getPriceEq(tokenq, token2):
	try:
		urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + token2)
	except:
		return -1
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
		self.fee = 0


order_list = []

with urllib.request.urlopen(availible_pairs_url) as response:
	jsn = response.read()
	availible_pairs = json.loads(jsn);
	availible_pairs = availible_pairs["data"] #пары доступных пар для обмена

for token in availible_pairs:
	for tkn in availible_pairs:
		if (token != tkn):
			print(token, tkn)
			token1 = token
			token2 = tkn
			token1_amount = getAmount(token1, token2)
			eth_price = getPriceEth(token1, token2)
			eq_price = getPriceEq(token1, token2)
			if (token1_amount == -1 or eth_price == -1 or eq_price == -1):
				continue;	
			order = Order(token1, token2, token1_amount, eth_price, eq_price)
			order_list.append(order)
			print(tkn, token)
			token1 = tkn
			token2 = token
			token1_amount = getAmount(token1, token2)
			eth_price = getPriceEth(token1, token2)
			eq_price = getPriceEq(token1, token2)
			if (token1_amount == -1 or eth_price == -1 or eq_price == -1):
				continue;	
			order = Order(token1, token2, token1_amount, eth_price, eq_price)
			order_list.append(order)
	print (pair, availible_pairs[pair])
	token1 = pair
	token2 = availible_pairs[pair]
	token1_amount = getAmount(token1, token2)
	eth_price = getPriceEth(token1, token2)
	eq_price = getPriceEq(token1, token2)
	order = Order(token1, token2, token1_amount, eth_price, eq_price)
	order_list.append(order)



	
print(order_list)