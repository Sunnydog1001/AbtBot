from orderbook import Orderbook
from order import Order
from strategy import find_best_match

def add_order(order, Orderbook):
    Orderbook.add_order_to_orderbook(order)

main_orderbook = Orderbook()
ExampleBook = Orderbook()
example = Order("RadarRelay", "WETH", "DAI", 10, 7.5, 137.1, 0)
add_order(example, ExampleBook)
example2 = Order("RadarRelay", "WETH", "DAI", 8, 7.5, 137.1, 0)
add_order(example2, ExampleBook)
example3 = Order("Bancor", "BTC", "RVN", 2100, 0.0002, 0.00001131, 0)
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

example4 = Order("RadarRelay", "WETH", "DAI", 10, 7.5, 1000, 0)
add_order(example4, ExampleBook)
example5 = Order("Bancor", "DAI", "WETH", 10, 0.02, 0.002, 0)
add_order(example5, ExampleBook)

print(find_best_match("WETH", "DAI"))