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

# This creates and fills the book variables
positions = e.get_positions()
A_vol = positions[instrument_A]
B_vol = positions[instrument_B]
delta_p = A_vol + B_vol
book_A = e.get_last_price_book(instrument_A)
book_B = e.get_last_price_book(instrument_B)
try:
    price_bid_A = book_A.bids[0].price
    price_bid_B = book_B.bids[0].price
    price_ask_A = book_A.asks[0].price
    price_ask_B = book_B.asks[0].price
    vol_bid_A = book_A.bids[0].volume
    vol_bid_B = book_B.bids[0].volume
    vol_ask_A = book_A.asks[0].volume
    vol_ask_B = book_B.asks[0].volume
except IndexError:
    continue

start_pnl = e.get_pnl()

i = 0

while i < 10000:
    updatePricePositions()
    if i != 0: 
        remove_outstanding()
    if  0.2< price_bid_B - price_ask_A:
        order_volume = min([200 - A_vol, 200 + B_vol, vol_ask_A, vol_bid_B, 40])

        print (f"Order Vol: {order_volume}")
        # WE need to scale the order volumes here in order to match delta p. (Lots of ifs, and watch the 200s in the order vol lists)
        if order_volume > 0:
            e.insert_order(instrument_A, price=price_ask_A, volume=order_volume, side='bid', order_type='limit')
            e.insert_order(instrument_B, price=price_bid_B, volume=order_volume, side='ask', order_type='limit')
            print (f"Buying A: {price_bid_B - price_ask_A}")
            print(e.get_positions())
            print (round(e.get_pnl() - start_pnl,1))
    elif  0.2 < price_bid_A - price_ask_B:
        order_volume = min([200 + A_vol, 200 - B_vol, vol_bid_A, vol_ask_B, 40])
        print (f"Order Vol: {order_volume}")
        if order_volume > 0:
            e.insert_order(instrument_B, price=price_ask_B, volume=order_volume, side='bid', order_type='limit')
            e.insert_order(instrument_A, price=price_bid_A, volume=order_volume, side='ask', order_type='limit')
            print (f"Buying B: {price_bid_A - price_ask_B}")
            print(e.get_positions())
            print (round(e.get_pnl() - start_pnl,1))
    
    
    i += 1
    time.sleep(1)
    
    
    
def remove_outstanding():
    # Removes the outstanding limit orders
    try:
        outstanding = e.get_outstanding_orders(instrument_A)
    for o in outstanding:
        e.delete_order(instrument_id=instrument_A, o)
    outstanding = e.get_outstanding_orders(instrument_B)
    for o in outstanding:
        e.delete_order(instrument_id=instrument_A, o)
    except IndexError:
        continue
    
    
def small_trades():
    gap = max([price_bid_B - price_ask_A, price_bid_A - price_ask_B])
    gap = gap/2
    #The gaps should be greater than 0  - we want it to be as large as the smallest price increment
    if gap>= 0.1:
            # We set limit orders here, and need to manage volume by delta_p:
            # We also need to deal with previous limits
        if A_vol > 0:
            # In this case we want to sell A and buy B:
            if abs(delta_p) != 10:
                e.insert_order(instrument_B, price=(price_bid_B-gap), volume=10 - delta_p, side='bid', order_type='limit')
                e.insert_order(instrument_A, price=(price_ask_A + gap), volume=10 + delta_p, side='ask', order_type='limit')
            elif delta_p == 10:
                e.insert_order(instrument_B, price=(price_bid_B-gap), volume=10, side='bid', order_type='limit')
                e.insert_order(instrument_A, price=(price_ask_A + gap), volume=20, side='ask', order_type='limit')
        elif B_vol > 0:
            # In this case we want to sell B and buy A:
            if abs(delta_p) != 10:
                e.insert_order(instrument_A, price=(price_bid_A-gap), volume=10 - delta_p, side='bid', order_type='limit')
                e.insert_order(instrument_B, price=(price_ask_B + gap), volume=10 + delta_p, side='ask', order_type='limit')
            elif delta_p == 10:
                e.insert_order(instrument_A, price=(price_bid_A-gap), volume=10, side='bid', order_type='limit')
                e.insert_order(instrument_B, price=(price_ask_B + gap), volume=20, side='ask', order_type='limit')
                    
                    
def updatePricePositions() # use this to find the latest bid prices, ask prices and delta p
    positions = e.get_positions()
    A_vol = positions[instrument_A]
    B_vol = positions[instrument_B]
    delta_p = A_vol + B_vol
    book_A = e.get_last_price_book(instrument_A)
    book_B = e.get_last_price_book(instrument_B)
    try:
        price_bid_A = book_A.bids[0].price
        price_bid_B = book_B.bids[0].price
        price_ask_A = book_A.asks[0].price
        price_ask_B = book_B.asks[0].price
        vol_bid_A = book_A.bids[0].volume
        vol_bid_B = book_B.bids[0].volume
        vol_ask_A = book_A.asks[0].volume
        vol_ask_B = book_B.asks[0].volume
    except IndexError:
        continue
    
