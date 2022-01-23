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

# This is the reset function in order to get us to a 0 position
print(e.get_positions())
for s, p in e.get_positions().items():
    if p > 0:
        e.insert_order(s, price=1, volume=p, side='ask', order_type='ioc')
    elif p < 0:
        e.insert_order(s, price=100000, volume=-p, side='bid', order_type='ioc')  
print(e.get_positions())

pnl_tracker = []

i = 0
while i < 10:
    book_A = e.get_last_price_book(instrument_A)
    book_B = e.get_last_price_book(instrument_B)
    
    price_bid_A = book_A.bids[0].price
    price_bid_B = book_B.bids[0].price
    price_ask_A = book_A.asks[0].price
    price_ask_B = book_B.asks[0].price
    
    
    
    if price_ask_A < price_ask_B:
        e.insert_order(instrument_A, price=price_ask_A, volume=1, side='bid', order_type='limit')
        e.insert_order(instrument_B, price=price_ask_B, volume=1, side='ask', order_type='limit')
    elif price_ask_B > price_ask_A:
        e.insert_order(instrument_B, price=price_ask_B, volume=1, side='bid', order_type='limit')
        e.insert_order(instrument_A, price=price_ask_A, volume=1, side='ask', order_type='limit')
    
    pnl = e.get_pnl()
    pnl_tracker.append((i, pnl))
    if i >= 1:
        print(pnl_tracker[i][1]-pnl_tracker[0][1])
    positions = e.get_positions()
    
    print(positions)
    time.sleep(0.5)
    i += 1

positions = e.get_positions()
print("\nFinal:")
print(positions)
print(pnl_tracker[-1][1]-pnl_tracker[0][1])