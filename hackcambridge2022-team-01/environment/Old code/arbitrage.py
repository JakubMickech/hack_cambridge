#arbitrage

from optibook.synchronous_client import Exchange

import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful.")

e = Exchange()
a = e.connect()
print("connected")

instrument_A = 'PHILIPS_A'
instrument_B = 'PHILIPS_B'
instrument_id = instrument_B


def limit_sell(instrument, price=1, volume=1):
    # Insert ask limit order - This trades against any current orders, and any remainders become new resting orders in the book
    # Use this to sell.
    result = e.insert_order(instrument, price=price, volume=volume, side='ask', order_type='limit')
    print(f"Order Id: {result}")

def limit_buy(instrument, price=1, volume=1):
    # Insert bid limit order - This trades against any current orders, and any remainders become new resting orders in the book
    # Use this to buy.
    result = e.insert_order(instrument, price=price, volume=volume, side='bid', order_type='limit')
    print(f"Order Id: {result}")
    
def ioc_sell(volume=1):
    # Insert ask limit order - This trades against any current orders, and any remainders become new resting orders in the book
    # Use this to sell.
    result = e.insert_order(instrument, price=100, volume=volume, side='ask', order_type='ioc')
    print(f"Order Id: {result}")

def ioc_buy(instrument, price=1, volume=1):
    # Insert bid limit order - This trades against any current orders, and any remainders become new resting orders in the book
    # Use this to buy.
    result = e.insert_order(instrument_A, price=price, volume=volume, side='bid', order_type='ioc')
    print(f"Order Id: {result}")

book_A = e.get_last_price_book(instrument_A)    
book_B = e.get_last_price_book(instrument_B)
a_bid = book_A.bids
b_bid = book_B.bids


a_ask = book_A.asks
b_ask = book_B.asks


print("This is the best A buying price offered by the market; we want to sell to the highest bid", a_bid[0])
print("B", b_bid[0])

print("This is the best A selling price offered by the market; we want to buy from the lowest ask", a_ask[0])
print("B", b_ask[0])

a_best_bid_price = a_bid[0].price
b_best_bid_price = b_bid[0].price

a_best_ask_price = a_ask[0].price
b_best_ask_price = b_ask[0].price

if a_best_bid_price < b_best_bid_price:
    # we want to sell to b
    limit_sell(instrument_B, b_best_bid_price)
elif a_best_bid_price > b_best_bid_price:
    # we want to sell to a
    limit_sell(instrument_A, a_best_bid_price)
    
if a_best_ask_price < b_best_ask_price:
    # we want to buy from a
    limit_buy(instrument_A, a_best_ask_price)
elif a_best_ask_price > b_best_ask_price:
    # we want to buy from b
    limit_buy(instrument_B, b_best_ask_price)
    
pnl = e.get_pnl()
print(pnl)