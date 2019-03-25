from bittrex.bittrex import Bittrex, API_V1_1, API_V2_0
from order import Order

my_bittrex = Bittrex("bcffcecbc9dd44f3b7000c7ebd11e1f4", "41a3b9169b754a32a1b56604ded87477",
                     api_version=API_V1_1)

def get_info(orderbook):
    markets = my_bittrex.get_markets()['result']

    for market in markets[:10]:
        result = my_bittrex.get_orderbook(market['MarketName'])['result']

        buy_orders = result['buy']
        sell_orders = result['sell']

        print("Downloading data...")

        for buy_order in buy_orders:
            order = Order("Bittrex", market['BaseCurrency'], market['MarketCurrency'],
                          float(buy_order['Quantity']), -1, 1 / float(buy_order['Rate']), 0)

            orderbook.add_order(order)

        for sell_order in sell_orders:
            order = Order("Bittrex", market['BaseCurrency'], market['MarketCurrency'],
                          float(sell_order['Quantity']), -1, 1 / float(sell_order['Rate']), 0)

            orderbook.add_order(order)