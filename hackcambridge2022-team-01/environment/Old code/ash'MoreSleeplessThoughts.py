from optibook.synchronous_client import Exchange
import logging
import time

# Sets Logger
logger = logging.getLogger('client')
logger.setLevel('ERROR')
 
# Connects to the exchange
print("Setup was successful.")
e = Exchange()
a = e.connect()
print("Connected to exchange.")

# Sets up the instrument variables
instrument_A = "PHILIPS_A"
instrument_B = "PHILIPS_B"
times = []
pricesBuyA = []
print(e.get_positions())
i = 0
while i < 60:
    book_A = e.get_last_price_book(instrument_A)
    book_B = e.get_last_price_book(instrument_B)
    time = book_A.timestamp
    print("running")
    try:
        price_buy_A = book_A.bids[0].price
    except IndexError:
        continue
    try:
        price_buy_B = book_B.bids[0].price
    except IndexError:
        continue
    try:
        price_sell_A = book_A.asks[0].price
    except IndexError:
        continue
    try:
        price_sell_B = book_B.asks[0].price
    except IndexError:
print("running")