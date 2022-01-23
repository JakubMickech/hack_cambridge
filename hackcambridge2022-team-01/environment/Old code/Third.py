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

start_pnl = e.get_pnl()

i = 0
while i < 10000:
    
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
    #print(price_ask_A - price_bid_B, price_ask_B - price_bid_A)
    #if (price_ask_A - price_bid_B < 0)or ( price_ask_B - price_bid_A < 0):
     #   print ("Sale Possible")
        
    if  0.2< price_bid_B - price_ask_A:
        # We buy as much A as we can, provided it's less than 200, the best offer has the capacity in both A and B:
        order_volume = min([200 - A_vol, 200 + B_vol, vol_ask_A, vol_bid_B, 40])
        print (f"Order Vol: {order_volume}")
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
    time.sleep(0.15)