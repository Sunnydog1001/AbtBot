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

    @staticmethod
    def _normalize_chain(chain):
        for i in range(1, len(chain)):
            k = chain[i].volume / (chain[i - 1].volume * chain[i - 1].price)

            if k < 1:
                for j in range(i):
                    chain[j].volume *= k
            else:
                chain[i].volume /= k


    @staticmethod
    def _print_chain(chain, original_chain, coef):

        print(original_chain)
        print(f"Coefficient: {coef:.4E}")

        # print(original_chain)

        print(f"{chain[0].volume:10.4E} {chain[0].bid_name} "
              f"\t\t{chain[0].dex_name}"
              f"{chain[0].volume * chain[0].price:10.4E} {chain[0].ask_name}", end="")

        for order in chain[1:]:
            print(f"\t\t{order.dex_name}"
                  f"{order.volume * order.price:10.4E} {order.ask_name}", end="")

        print()

    def _find_path(self, from_token, to_token, coef, path_len, chain, visited):
        if path_len == 0 and from_token == to_token:
            if coef > 1.0:
                original_chain = chain.copy()
                Orderbook._normalize_chain(chain)
                Orderbook._print_chain(chain, original_chain, coef)

            return

        if from_token in visited:
            return

        visited.add(from_token)

        for (token1, token2) in self.token_pairs:
            if token1 != from_token:
                continue

            for order in self.orders_dict[(token1, token2)]:
                chain.append(order)
                self._find_path(token2, to_token, coef * order.price, path_len - 1, chain, visited)
                chain.pop()

        visited.remove(from_token)

    def find_arbitrary_situations(self, k):
        visited = set()

        for token in self.tokens:
            self._find_path(token, token, 1, k, [], visited)
            visited.clear()




