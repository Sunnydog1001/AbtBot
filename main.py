from orderbook import Orderbook
from order import Order
import radar_relay
import uniswap
import bancor
import bit

main_orderbook = Orderbook()

# example6 = Order("Radar Relay", "A", "B", 10, -1, 5, 0)
# example7 = Order("Radar Relay", "B", "C", 30, -1, 0.1, 0)
# example8 = Order("Radar Relay", "C", "A", 3, -1, 2.1, 0)
# main_orderbook.add_order(example6)
# main_orderbook.add_order(example7)
# main_orderbook.add_order(example8)

radar_relay.get_info(main_orderbook)
uniswap.get_info(main_orderbook)
# bancor.get_info(main_orderbook)
bit.get_info(main_orderbook)

main_orderbook.find_arbitrary_situations(2)
main_orderbook.find_arbitrary_situations(3)
