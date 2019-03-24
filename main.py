from orderbook import Orderbook
from order import Order
import radar_relayer

main_orderbook = Orderbook()

# example6 = Order("Radar Relay", "A", "B", 10, -1, 5, 0)
# example7 = Order("Radar Relay", "B", "C", 30, -1, 0.1, 0)
# example8 = Order("Radar Relay", "C", "A", 3, -1, 2.1, 0)
#
# example_book.add_order(example6)
# example_book.add_order(example7)
# example_book.add_order(example8)

radar_relayer.get_info(main_orderbook)
main_orderbook.find_arbitrary_situations(2)