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

print(e.get_positions())
for s, p in e.get_positions().items():
    if p > 0:
        e.insert_order(s, price=1, volume=p, side='ask', order_type='ioc')
    elif p < 0:
        e.insert_order(s, price=100000, volume=-p, side='bid', order_type='ioc')  
print(e.get_positions())


# Sets up the instrument variables
instrument_A = "PHILIPS_A"
instrument_B = "PHILIPS_B"

# Getting price books
book_A = e.get_last_price_book(instrument_A)
book_B = e.get_last_price_book(instrument_B)

# Getting the current prices
if len(book_B.asks) > 0:
    ask_price_B = book_B.asks[0].price
if len(book_B.bids) > 0:    
    bid_price_B = book_B.bids[0].price
if len(book_A.asks) > 0:
    ask_price_A = book_A.asks[0].price
if len(book_A.bids) > 0:   
    bid_price_A = book_A.bids[0].price

print(ask_price_B, bid_price_B, ask_price_A, bid_price_A)

gap_A = ask_price_A - bid_price_A
gap_B = ask_price_B - bid_price_B

# Get difference between the prices. Determines whether we want to be short or long on B
differenceAB = (ask_price_A + bid_price_A) / 2 - (ask_price_B + bid_price_B) / 2

print(differenceAB)

# Setting up base orders in B - the less liquid market
if differenceAB > 0:
    e.insert_order(instrument_B, price=(bid_price_B + gap_B*0.1*differenceAB), volume=1, side='bid', order_type='limit')
    print("Inserting order Bid ", bid_price_B + gap_B*0.1*differenceAB)
else:
    e.insert_order(instrument_B, price=(ask_price_B - gap_B*0.1*differenceAB), volume=1, side='ask', order_type='limit')
    print("Inserting order Ask ", ask_price_B - gap_B*0.1*differenceAB)

for i in range(1000):
    trades_B = e.poll_new_trades(instrument_B)
    
    # Put in hedge orders in instrument A to protect against losses - if these trades go through, we should already make profit
    if len(trades_B) > 0:
        for t in trades_B:
            print(t)
            if t.side == 'bid':
                e.insert_order(instrument_A, price=(t.price + 0.1), volume=1, side='ask', order_type='limit')
            else:
                e.insert_order(instrument_A, price=(t.price - 0.1), volume=1, side='bid', order_type='limit')
    
    # Getting price books
    book_A = e.get_last_price_book(instrument_A)
    book_B = e.get_last_price_book(instrument_B)
    
    # Getting the current prices
    ask_price_B = book_B.asks[0].price
    bid_price_B = book_B.bids[0].price
    ask_price_A = book_A.asks[0].price
    bid_price_A = book_A.bids[0].price
    
    gap_A = ask_price_A - bid_price_A
    gap_B = ask_price_B - bid_price_B
    
    positions = e.get_positions()
    A_vol = positions[instrument_A]
    B_vol = positions[instrument_B]
    delta_p = A_vol + B_vol
    
    print(positions)
    
    # Get difference between the prices. Determines whether we want to be short or long on B
    differenceAB = (ask_price_A + bid_price_A) / 2 - (ask_price_B + bid_price_B) / 2
    
    if (i % 10 == 0) and delta_p < 10 and 0 < len(e.get_outstanding_orders(instrument_B)) - delta_p:
        print("New order of B, differenceAB", differenceAB)
        if differenceAB > 0:
            e.insert_order(instrument_B, price=(bid_price_B + gap_B*0.1*differenceAB), volume=1, side='bid', order_type='limit')
        else:
            e.insert_order(instrument_B, price=(ask_price_B + gap_B*0.1*differenceAB), volume=1, side='ask', order_type='limit')
    
    time.sleep(0.2)


    
    