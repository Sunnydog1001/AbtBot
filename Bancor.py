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

def getPriceEth(token1, token2):
	try:
		urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + "ETH")
	except:
		print("")
		return -1
	with urllib.request.urlopen(tiker1 + token1 + tiker2 + token2 + tiker3 + "ETH") as response:
		jsn = response.read()
		info = json.loads(jsn)
		info = info["data"]
	return info["price24h"]

def getPriceEq(token1, token2):
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
	def __init__(self, bid = "",  ask = "", volume = 0, eth_price = 0,
		price = 0):
		self.dex_name = "Bancor"
		self.bid_name = bid
		self.ask_name = ask
		self.volume = volume
		self.eth_price = eth_price
		self.price = price
		self.fee = 0

def make_order(token1, token2):
	token1_amount = getAmount(token1, token2)
	eth_price = getPriceEth(token1, token2)
	eq_price = getPriceEq(token1, token2)
	if (token1_amount == -1 or eth_price == -1 or eq_price == -1):
		return -1;	
	order = Order(token1, token2, token1_amount, eth_price, eq_price)
	return order

order_list = []

with urllib.request.urlopen(availible_pairs_url) as response:
	jsn = response.read()
	availible_pairs = json.loads(jsn);
	availible_pairs = availible_pairs["data"]

for token in availible_pairs:

	print(token, availible_pairs[token])
	order = make_order(token, availible_pairs[token])
	if (order == -1):
		continue
	order_list.append(order)
	
	print(availible_pairs[token], token)	
	order = make_order(availible_pairs[token], token)
	if (order == -1):
		continue
	order_list.append(order)


	for tkn in availible_pairs:
		if (token != tkn):
			
			print(token, tkn)
			order = make_order(token, tkn)
			if (order == -1):
				continue
			order_list.append(order)

			print(tkn, token)	
			order = make_order(tkn, token)
			if (order == -1):
				continue
			order_list.append(order)
	
print(order_list)