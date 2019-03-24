from order import Order

class Pair(object):

    def __init__(self):
        self.bid_book = {} # bid_book = {price : [volume, eth_price, fee]}

    def add_order(self, order):
        if order.price in self.bid_book:
            self.bid_book[order.price][0] += order.volume
        else:
            self.bid_book[order.price] = [order.volume, order.eth_price, order.fee]

class Tokenbook(object):

    def __init__(self):
        self.pairs = {}  # PairName : PairObject

    def add_order(self, order):
        if order.ask_name in self.pairs:
            self.pairs[order.ask_name].add_order(order)
        else:
            self.pairs[order.ask_name] = Pair()
            self.pairs[order.ask_name].add_order(order)

class DEX(object):

    def __init__(self):
        self.tokens = {}  # TokenName : TokenObject

    def add_order(self, order):
        if order.bid_name in self.tokens:
            self.tokens[order.bid_name].add_order(order)
        else:
            self.tokens[order.bid_name] = Tokenbook()
            self.tokens[order.bid_name].add_order(order)


class Orderbook(object):

    def __init__(self):
        self.DEXs = {}
        self.orders_dict = {}
        self.token_pairs = set()
        self.tokens = set()

    def add_order(self, order):
        if order.dex_name in self.DEXs:
            self.DEXs[order.dex_name].add_order(order)
        else:
            self.DEXs[order.dex_name] = DEX()
            self.DEXs[order.dex_name].add_order(order)

        if (order.bid_name, order.ask_name) not in self.orders_dict:
            self.orders_dict[(order.bid_name, order.ask_name)] = [order]
        else:
            self.orders_dict[(order.bid_name, order.ask_name)].append(order)

        self.token_pairs.add((order.bid_name, order.ask_name))
        self.tokens.add(order.bid_name)
        self.tokens.add(order.ask_name)

    def find_path(self, from_token, to_token, coef, path_len, chain, visited):
        if path_len == 0 and from_token == to_token:
            if coef > 1.0:
                print(coef)
                print(chain)

            return

        visited.add(from_token)

        for (token1, token2) in self.token_pairs:
            if token1 != from_token:
                continue

            if token2 in visited and token2 != to_token:
                continue

            for order in self.orders_dict[(token1, token2)]:
                chain.append(order)
                self.find_path(token2, to_token, coef * order.price, path_len - 1, chain, visited)
                chain.pop()

        visited.remove(from_token)

    def find_arbitrary_situations(self, k):
        visited = set()

        for token in self.tokens:
            self.find_path(token, token, 1, k, [], visited)




