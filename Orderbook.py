#from RaderRelay import order

class Pair(object):
    def __init__(self):
        self.bid_book = {} # bid_book = {price : [volume, eth_price, fee]}

    def add_order_to_Pair(self, order):
        if order.price in self.bid_book:
            self.bid_book[order.price][0] += order.volume
        else:
            self.bid_book[order.price] = [order.volume, order.eth_price, order.fee]

class Tokenbook(object):
    def __init__(self):
        self.Pairs = {}  # PairName : PairObject

    def add_order_to_Tokenbook(self, order):
        if order.ask_name in self.Pairs:
            self.Pairs[order.ask_name].add_order_to_Pair(order)
        else:
            self.Pairs[order.ask_name] = Pair()
            self.Pairs[order.ask_name].add_order_to_Pair(order)


class DEX(object):
    def __init__(self):
        self.tokens = {}  # TokenName : TokenObject

    def add_order_to_DEX(self, order):
        if order.bid_name in self.tokens:
            self.tokens[order.bid_name].add_order_to_Tokenbook(order)
        else:
            self.tokens[order.bid_name] = Tokenbook()
            self.tokens[order.bid_name].add_order_to_Tokenbook(order)


class Orderbook(object):
    def __init__(self):
        self.DEXs = {}  # DEXName : DEXObject

    def add_order_to_orderbook(self, order):
        if order.dex_name in self.DEXs:
            self.DEXs[order.dex_name].add_order_to_DEX(order)
        else:
            self.DEXs[order.dex_name] = DEX()
            self.DEXs[order.dex_name].add_order_to_DEX(order)


class order(object):
    def __init__(self, dex, bid, ask, volume, eth_price, price, fee):
        self.dex_name = dex
        self.bid_name = bid
        self.ask_name = ask
        self.volume = volume
        self.price = price
        self.eth_price = eth_price
        self.fee = fee


def add_order(order, Orderbook):
    Orderbook.add_order_to_orderbook(order)


def find_best_match(token1, token2):
    best_bid = best_ask = 0
    for dex in ExampleBook.DEXs:
        if token1 in ExampleBook.DEXs[dex].tokens and token2 in ExampleBook.DEXs[dex].tokens[token1].Pairs:
            book_bid = sorted(ExampleBook.DEXs[dex].tokens[token1].Pairs[token2].bid_book.items())
            if book_bid[-1][0] > best_bid:
                best_bid = book_bid[-1][0]
        if token2 in ExampleBook.DEXs[dex].tokens and token1 in ExampleBook.DEXs[dex].tokens[token2].Pairs:
            book_ask = sorted(ExampleBook.DEXs[dex].tokens[token2].Pairs[token1].bid_book.items())
            if book_ask[-1][0] > best_ask:
                best_ask = book_ask[-1][0]
    if best_bid > best_ask:
        k = best_bid / (1 / best_ask)
    elif best_ask > best_bid:
        k = best_ask / (1 / best_bid)
    else: k = 1
    return [best_bid, best_ask, k] #если коэффициент > 1, возможна прибыльная сделка


ExampleBook = Orderbook()
example = order("RadarRelay", "WETH", "DAI", 10, 7.5, 137.1, 0)
add_order(example, ExampleBook)
example2 = order("RadarRelay", "WETH", "DAI", 8, 7.5, 137.1, 0)
add_order(example2, ExampleBook)
example3 = order("Bancor", "BTC", "RVN", 2100, 0.0002, 0.00001131, 0)
add_order(example3, ExampleBook)
for dex in ExampleBook.DEXs:
    print(dex, ":")
    for token in ExampleBook.DEXs[dex].tokens:
        for pair in ExampleBook.DEXs[dex].tokens[token].Pairs:
            print(token, "-", pair, ":")
            for prc in ExampleBook.DEXs[dex].tokens[token].Pairs[pair].bid_book:
                print(prc, ": [volume, eth_price, fee]:", ExampleBook.DEXs[dex].tokens[token].Pairs[pair].bid_book[prc], "\n")
#RadarRelay :
#WETH - DAI :
#137.1 : [volume, eth_price, fee]: [18, 7.5, 0] 

#Bancor :
#BTC - RVN :
#1.131e-05 : [volume, eth_price, fee]: [2100, 0.0002, 0] 
example4 = order("RadarRelay", "WETH", "DAI", 10, 7.5, 1000, 0)
add_order(example4, ExampleBook)
example5 = order("Bancor", "DAI", "WETH", 10, 0.02, 0.002, 0)
add_order(example5, ExampleBook)
print(find_best_match("WETH", "DAI"))
#[1000, 0.002, 2.0]
