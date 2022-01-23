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

pnl_tracker = e.get_pnl()

book_A = e.get_last_price_book(instrument_A)
price_buy_A  = book_A.bids[0].price
price_sell_A = book_A.asks[0].price
gap = price_sell_A - price_buy_A
positions = e.get_positions()

limit_buy_A = price_sell_A-(gap*0.02)
limit_sell_A = price_buy_A+(gap*0.02)

# This is the loop for updating the limits   
i = 0
while i < 30:
    # Get the prices and positions updated
    book_A = e.get_last_price_book(instrument_A)
    price_buy_A  = book_A.bids[0].price
    price_sell_A = book_A.asks[0].price
    gap = price_sell_A - price_buy_A
    positions = e.get_positions()
    A_vol = 
    print(price_buy_A, price_sell_A)
    
    # This is the volume of the A holdings
    A_vol = positions[instrument_A]
    
    # Here we check if we have any outstanding orders
    if i != 0:
        outstanding = e.get_outstanding_orders(instrument_A)
        for o in outstanding:
            e.delete_order(instrument_id=instrument_A, order_id=o)
        
    # Here we put new order in
    if (A_vol) == 10:
        sell_order = e.insert_order(instrument_A, price=min(price_sell_A-(gap*0.02), limit_sell_A), volume=A_vol + 10, side='ask', order_type='limit')
    elif (A_vol) == -10:
        buy_order = e.insert_order(instrument_A, price=max(price_buy_A+(gap*0.02), limit_buy_A), volume= 10 - A_vol , side='bid', order_type='limit')
    else:
        sell_order = e.insert_order(instrument_A, price=price_sell_A-(gap*0.02), volume=A_vol + 10, side='ask', order_type='limit')
        buy_order = e.insert_order(instrument_A, price=price_buy_A+(gap*0.02), volume= 10 - A_vol , side='bid', order_type='limit')
    
    positions = e.get_positions()
    
    print(positions)
    pnl = e.get_pnl()
    pnl_tracker.append((i, pnl))
    if i >= 1:
        print(pnl_tracker[i][1]-pnl_tracker[0][1])
    
    time.sleep(1)
    i += 1

print("\nFinal:")
profit = 0
price_history = e.get_trade_history(instrument_A)
for p in price_history:
    if p.side == 'ask':
        profit += p.price * p.volume
        print("profit:", profit)
    else: 
        profit -= p.price * p.volume
for t in price_history:
    print(f"[TRADED {t.instrument_id}] price({t.price}), volume({t.volume}), side({t.side})")
    
print(profit)

positions = e.get_positions()
print(positions)
print(pnl_tracker[-1][1]-pnl_tracker[0][1])
    
    
