from order import Order

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
        self.DEXs = {}
        self.order_dict = {}

    def add_order_to_orderbook(self, order):
        if order.dex_name in self.DEXs:
            self.DEXs[order.dex_name].add_order_to_DEX(order)
        else:
            self.DEXs[order.dex_name] = DEX()
            self.DEXs[order.dex_name].add_order_to_DEX(order)

        if (order.ask_name, order.bid_name) not in self.order_dict:
            self.order_dict[order.ask_name, order.bid_name] = [order]
        else:
            self.order_dict[(order.ask_name, order.bid_name)].append(order)

def add_order(order, Orderbook):
    Orderbook.add_order_to_orderbook(order)
