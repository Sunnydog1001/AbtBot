
def find_best_match(orderbook, token1, token2):
    best_bid = best_ask = 0
    for dex in orderbook.DEXs:

        if token1 in orderbook.DEXs[dex].tokens and token2 in orderbook.DEXs[dex].tokens[token1].Pairs:
            book_bid = sorted(orderbook.DEXs[dex].tokens[token1].Pairs[token2].bid_book.items())
            if book_bid[-1][0] > best_bid:
                best_bid = book_bid[-1][0]

        if token2 in orderbook.DEXs[dex].tokens and token1 in orderbook.DEXs[dex].tokens[token2].Pairs:
            book_ask = sorted(orderbook.DEXs[dex].tokens[token2].Pairs[token1].bid_book.items())
            if book_ask[-1][0] > best_ask:
                best_ask = book_ask[-1][0]

    if best_bid > best_ask:
        k = best_bid / (1 / best_ask)
    elif best_ask > best_bid:
        k = best_ask / (1 / best_bid)
    else: k = 1

    return [best_bid, best_ask, k] #если коэффициент > 1, возможна прибыльная сделка

def find_arbitrary_sitations(orderbook):
    pass