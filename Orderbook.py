class Pair(object):
    def __init__(self):
        self.bid_book = {} # bid_book = {price : [volume, [ids]]}


    def add_order_to_Pair(self, order):
        if order.price in self.bid_book:
            self.bid_book[order.price][0] += order.volume
            self.bid_book[order.price][1].append(order.id)
        else:
            self.bid_book[order.price] = [order.volume, [order.id]]


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
    def __init__(self, dex, id, price, vol, bid, ask):
        self.dex_name = dex
        self.bid_name = bid
        self.ask_name = ask
        self.volume = vol
        self.id = id
        self.price = price


def add_order(order, Orderbook):
    Orderbook.add_order_to_orderbook(order)

    
ExampleBook = Orderbook()
example = order("RadarRelay", "1218278hgihfh3uf3$ygf8e", 137.1, 10, "WETH", "DAI")
add_order(example, ExampleBook)
example2 = order("RadarRelay", "18778778hgihfh3uf3$ygf76g", 137.1, 1, "WETH", "DAI")
add_order(example2, ExampleBook)
example3 = order("Bancor", "838gd78fgf78egf78idfd8k0", 0.00001131, 2100, "BTC", "RVN")
add_order(example3, ExampleBook)
for dex in ExampleBook.DEXs:
    print(dex, ":")
    for token in ExampleBook.DEXs[dex].tokens:
        for pair in ExampleBook.DEXs[dex].tokens[token].Pairs:
            print(token, "-", pair, ":")
            for prc in ExampleBook.DEXs[dex].tokens[token].Pairs[pair].bid_book:
                print(prc, ": volume:", ExampleBook.DEXs[dex].tokens[token].Pairs[pair].bid_book[prc][0], "orderIds:", ExampleBook.DEXs[dex].tokens[token].Pairs[pair].bid_book[prc][1], "\n")
#RadarRelay :
#WETH - DAI :
#137.1 : volume: 11 orderIds: ['1218278hgihfh3uf3$ygf8e', '18778778hgihfh3uf3$ygf76g'] 

#Bancor :
#BTC - RVN :
#1.131e-05 : volume: 2100 orderIds: ['838gd78fgf78egf78idfd8k0'] 
