import bisect
import numpy as np

class DEX(object):
    def __init__(self):
        self._tokens = {}  # TokenName : TokenObject

    def sortby(self, attribute):
        return


class Orderbook(object):
    def __init__(self):
        self._DEXs = {}  # DEXName : DEXObject

    def sortby(self, attribute):
        return

class tokenbook(object):
    def __init__(self):
        self._bid_book = {}
        self._bid_book_prices = np.array([])
        self._ask_book = {}
        self._ask_book_prices = np.array([])
        self.confirm_modify_collector = np.array([])
        self.confirm_trade_collector = np.array([])
        self.trade_book = np.array([])
        self._order_index = 0
        self.traded = False
        self.volume = 0

    def add_order_to_book(self, order):
        book_order = {'order_id': order['order_id'], 'timestamp': order['timestamp'], 'type': order['type'],
                      'quantity': order['quantity'], 'side': order['side'], 'price': order['price']}
        if order['side'] == 'buy':
            book_prices = self._bid_book_prices
            book = self._bid_book
        else:
            book_prices = self._ask_book_prices
            book = self._ask_book
        if order['price'] in book_prices:
            book[order['price']]['num_orders'] += 1
            book[order['price']]['size'] += order['quantity']
            book[order['price']]['order_ids'].append(order['order_id'])
            book[order['price']]['orders'][order['order_id']] = book_order
        else:
            bisect.insort(book_prices, order['price'])
            book[order['price']] = {'num_orders': 1, 'size': order['quantity'], 'order_ids': [order['order_id']],
                                    'orders': {order['order_id']: book_order}}

    def _remove_order(self, order_side, order_price, order_id):
        if order_side == 'buy':
            book_prices = self._bid_book_prices
            book = self._bid_book
        else:
            book_prices = self._ask_book_prices
            book = self._ask_book
        is_order = book[order_price]['orders'].pop(order_id, None)
        if is_order:
            book[order_price]['num_orders'] -= 1
            book[order_price]['size'] -= is_order['quantity']
            book[order_price]['order_ids'].remove(is_order['order_id'])
            if book[order_price]['num_orders'] == 0:
                book_prices.remove(order_price)

    def _modify_order(self, order_side, order_quantity, order_id, order_price):
        book = self._bid_book if order_side == 'buy' else self._ask_book
        if order_quantity < book[order_price]['orders'][order_id]['quantity']:
            book[order_price]['size'] -= order_quantity
            book[order_price]['orders'][order_id]['quantity'] -= order_quantity
        else:
            self._remove_order(order_side, order_price, order_id)

    def _add_trade_to_book(self, resting_order_id, resting_timestamp, incoming_order_id, timestamp, price, quantity,
                           side):
        self.trade_book.append({'resting_order_id': resting_order_id, 'resting_timestamp': resting_timestamp,
                                'incoming_order_id': incoming_order_id, 'timestamp': timestamp, 'price': price,
                                'quantity': quantity, 'side': side})

    def _confirm_trade(self, timestamp, order_side, order_quantity, order_id, order_price):
        trader = order_id.partition('_')[0]
        self.confirm_trade_collector.append({'timestamp': timestamp, 'trader': trader, 'order_id': order_id,
                                             'quantity': order_quantity, 'side': order_side, 'price': order_price})

    def _confirm_modify(self, timestamp, order_side, order_quantity, order_id):
        trader = order_id.partition('_')[0]
        self.confirm_modify_collector.append({'timestamp': timestamp, 'trader': trader, 'order_id': order_id,
                                              'quantity': order_quantity, 'side': order_side})

    def process_order(self, order):
        self.confirm_modify_collector.clear()
        self.traded = False
        self._add_order_to_history(order)
        if order['type'] == 'add':
            if order['side'] == 'buy':
                if order['price'] >= self._ask_book_prices[0]:
                    self._match_trade(order)
                else:
                    self.add_order_to_book(order)
            else:
                if order['price'] <= self._bid_book_prices[-1]:
                    self._match_trade(order)
                else:
                    self.add_order_to_book(order)
        else:
            book_prices = self._bid_book_prices if order['side'] == 'buy' else self._ask_book_prices
            if order['price'] in book_prices:
                book = self._bid_book if order['side'] == 'buy' else self._ask_book
                if order['order_id'] in book[order['price']]['orders']:
                    self._confirm_modify(order['timestamp'], order['side'], order['quantity'], order['order_id'])
                    if order['type'] == 'cancel':
                        self._remove_order(order['side'], order['price'], order['order_id'])
                    else:
                        self._modify_order(order['side'], order['quantity'], order['order_id'], order['price'])

    def _match_trade(self, order):
        self.traded = True
        self.confirm_trade_collector.clear()
        if order['side'] == 'buy':
            book_prices = self._ask_book_prices
            book = self._ask_book
            remainder = order['quantity']
            while remainder > 0:
                if book_prices:
                    price = book_prices[0]
                    if order['price'] >= price:
                        book_order_id = book[price]['order_ids'][0]
                        book_order = book[price]['orders'][book_order_id]
                        if remainder >= book_order['quantity']:
                            self._confirm_trade(order['timestamp'], book_order['side'], book_order['quantity'],
                                                book_order['order_id'], book_order['price'])
                            self._add_trade_to_book(book_order['order_id'], book_order['timestamp'], order['order_id'],
                                                    order['timestamp'], book_order['price'],
                                                    book_order['quantity'], order['side'])
                            self._remove_order(book_order['side'], book_order['price'], book_order['order_id'])
                            remainder -= book_order['quantity']
                        else:
                            self._confirm_trade(order['timestamp'], book_order['side'], remainder,
                                                book_order['order_id'], book_order['price'])
                            self._add_trade_to_book(book_order['order_id'], book_order['timestamp'], order['order_id'],
                                                    order['timestamp'], book_order['price'],
                                                    remainder, order['side'])
                            self._modify_order(book_order['side'], remainder, book_order['order_id'],
                                               book_order['price'])
                            break
                    else:
                        order['quantity'] = remainder
                        self.add_order_to_book(order)
                        break
                else:
                    print('Ask Market Collapse with order {0}'.format(order))
                    break
        else:
            book_prices = self._bid_book_prices
            book = self._bid_book
            remainder = order['quantity']
            while remainder > 0:
                if book_prices:
                    price = book_prices[-1]
                    if order['price'] <= price:
                        book_order_id = book[price]['order_ids'][0]
                        book_order = book[price]['orders'][book_order_id]
                        if remainder >= book_order['quantity']:
                            self._confirm_trade(order['timestamp'], book_order['side'], book_order['quantity'],
                                                book_order['order_id'], book_order['price'])
                            self._add_trade_to_book(book_order['order_id'], book_order['timestamp'], order['order_id'],
                                                    order['timestamp'], book_order['price'],
                                                    book_order['quantity'], order['side'])
                            self._remove_order(book_order['side'], book_order['price'], book_order['order_id'])
                            remainder -= book_order['quantity']
                        else:
                            self._confirm_trade(order['timestamp'], book_order['side'], remainder,
                                                book_order['order_id'], book_order['price'])
                            self._add_trade_to_book(book_order['order_id'], book_order['timestamp'], order['order_id'],
                                                    order['timestamp'], book_order['price'],
                                                    remainder, order['side'])
                            self._modify_order(book_order['side'], remainder, book_order['order_id'],
                                               book_order['price'])
                            break
                    else:
                        order['quantity'] = remainder
                        self.add_order_to_book(order)
                        break
                else:
                    print('Bid Market Collapse with order {0}'.format(order))
                    break

    def sortby(self, attribute):
        return
