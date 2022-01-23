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


def limit_sell(volume=1):
    # Insert ask limit order - This trades against any current orders, and any remainders become new resting orders in the book
    # Use this to sell.
    result = e.insert_order(instrument_B, price=100, volume=volume, side='ask', order_type='limit')
    print(f"Order Id: {result}")

def limit_buy(price=1, volume=1):
    # Insert bid limit order - This trades against any current orders, and any remainders become new resting orders in the book
    # Use this to buy.
    result = e.insert_order(instrument_A, price=price, volume=volume, side='bid', order_type='limit')
    print(f"Order Id: {result}")
    
def ioc_sell(volume=1):
    # Insert ask limit order - This trades against any current orders, and any remainders become new resting orders in the book
    # Use this to sell.
    result = e.insert_order(instrument_B, price=100, volume=volume, side='ask', order_type='ioc')
    print(f"Order Id: {result}")

def ioc_buy(price=1, volume=1):
    # Insert bid limit order - This trades against any current orders, and any remainders become new resting orders in the book
    # Use this to buy.
    result = e.insert_order(instrument_A, price=price, volume=volume, side='bid', order_type='ioc')
    print(f"Order Id: {result}")

book_A = e.get_last_price_book(instrument_A)    
book_B = e.get_last_price_book(instrument_B)
b_bid = book_B.bids
for b in b_bid:
    print(b)

a_bid = book_A.bids
for a in a_bid:
    print(a)

print("A", book_A.bids)
print("B", book_B.bids)



price_buy_B = book_B.bids[0].price
print(price_buy_B)

limit_buy(price=price_buy_B)


 
