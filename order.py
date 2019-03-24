class Order(object):

    def __init__(self, dex_name:str, bid:str, ask:str, volume:float, eth_price:float, price:float, fee:float):
        self.dex_name = dex_name
        self.bid_name = bid
        self.ask_name = ask
        self.volume = volume
        self.eth_price = eth_price
        self.price = price
        self.fee = fee

    def __str__(self):
        return f"Order: giving {self.volume:.4E} {self.bid_name} for {self.volume * self.price:.4E} {self.ask_name}"

    def __repr__(self):
        return self.__str__()