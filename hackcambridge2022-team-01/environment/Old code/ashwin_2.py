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
profit = 0
while i < 60:
    book_A = e.get_last_price_book(instrument_A)
    book_B = e.get_last_price_book(instrument_B)
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
        continue
    print(price_buy_A)
    print(price_buy_B)
    print(price_sell_A)
    print(price_sell_B)
    print(price_buy_B<price_sell_A)
    if (price_buy_B<price_sell_A):
        print("loop run")
        positions = e.get_positions()
        positionA = positions["PHILIPS_A"]
        positionB = positions["PHILIPS_B"]
        print("Positions in B", positionB)
        if (positionA > -9) and (positionA < 9):
            e.insert_order(instrument_A, price=price_sell_A-0.5, volume=1, side='ask', order_type='ioc')
        if ((positionB < 9) and (positionB > -9)):
            e.insert_order(instrument_B, price=price_buy_B+0.5, volume=1, side='bid', order_type='ioc')

            
        positions = e.get_positions()
        for p in positions:
            print(p, positions[p])
    price_history = e.get_trade_history(instrument_A)
    for t in price_history:
        print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")
    profit = 0
    for p in price_history:
        if p.side == 'ask':
            profit += p.price * p.volume
            print("profit:", profit)
        elif p.side == "bid": 
            profit -= p.price * p.volume
    
    time.sleep(1)