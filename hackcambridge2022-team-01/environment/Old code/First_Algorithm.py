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
while i < 60:
    book_A = e.get_last_price_book(instrument_A)
    book_B = e.get_last_price_book(instrument_B)
    
    price_buy_A = book_A.bids[0].price
    price_buy_B = book_B.bids[0].price
    price_sell_A = book_A.asks[0].price
    price_sell_B = book_B.asks[0].price
    price_avg_A = (price_buy_A + price_sell_A) / 2
    price_avg_B = (price_buy_B + price_sell_B) / 2
    
    
    print(price_buy_A, price_buy_B)
    
    if price_avg_B > price_avg_A:
        e.insert_order(instrument_A, price=price_buy_A*1.05, volume=1, side='bid', order_type='ioc')
        e.insert_order(instrument_B, price=price_sell_B*0.95, volume=1, side='ask', order_type='ioc')
    else:
        e.insert_order(instrument_B, price=price_buy_B*1.05, volume=1, side='bid', order_type='ioc')
        e.insert_order(instrument_A, price=price_sell_A*0.95, volume=1, side='ask', order_type='ioc')
    
    pnl = e.get_pnl()
    pnl_tracker.append((i, pnl))
    if i >= 1:
        print(pnl_tracker[i][1]-pnl_tracker[i-1][1])
    positions = e.get_positions()
    
    print(positions)
    time.sleep(1)
    i += 1

positions = e.get_positions()
print(positions)
print(pnl_tracker[-1][1]-pnl_tracker[0][1])