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

# sets up variable to check if order taken place
OrderTakenPlace = False


# Sets up the instrument variables
instrument_A = "PHILIPS_A"
instrument_B = "PHILIPS_B"

# Getting price books
book_A = e.get_last_price_book(instrument_A)
book_B = e.get_last_price_book(instrument_B)

# Getting the current prices
ask_price_B = book_B.asks[0].price
ask_volume_B= book_B.asks[0].volume
bid_price_B = book_B.bids[0].price
bid_volume_B = book_B.bids[0].volume
ask_price_A = book_A.asks[0].price
ask_volume_A = book_A.asks[0].volume
bid_price_A = book_A.bids[0].price
bid_volume_A = book_A.bids[0].volume

print(ask_price_B, bid_price_B, ask_price_A, bid_price_A)

# here we find the spread in B and in A

gapInB = ask_price_B - bid_price_B
gapInA = ask_price_A - bid_price_A

# function to place order
# use last traded value
if (bid_price_B < bid_price_A):# means we should buy B as it should go up 
    volumeUsed = ask_volume_A
    if(ask_volume_A>bid_volume_B):
        volumeUsed = ask_volume_B
    e.insert_order(instrument_B, price=bid_price_B+gapInB*0.1, volume=volumeUsed, side='bid', order_type='ioc') # we are buying b
    e.insert_order(instrument_A, price=ask_price_A-gapInA*0.1, volume=volumeUsed, side='ask', order_type='ioc')
    # check both orders have gone through by getting positions 
    

    print(e.get_positions())
    positionA = positions["PHILIPS_A"]
    positionB = positions["PHILIPS_B"]
    totalPositions = positionA + positionB
    if totalPositions != 0:
        for s, p in e.get_positions().items():
            if p > 0:
                e.insert_order(s, price=1, volume=p, side='ask', order_type='ioc')
            elif p < 0:
                e.insert_order(s, price=100000, volume=-p, side='bid', order_type='ioc')  
        print(e.get_positions())
    
    # now either an order has been placed 
    
#run this function while an order has been placed
orderplacedA = e.poll_new_trades(instrument_A)
orderplacedB = e.poll_new_trades(instrument_B)
#initialise variables to hold values sold/bought for
valueABought = 0
totalBuyValueA = 0
valueBSold = 0
totalSaleValueB = 0
buyA = False
sellA = False
buyB = False
sellb = False

if orderplacedA.side == 'ask':  # if a was sold calc price it was sold for
    valueABought = orderplacedA.price
    totalBuyValueA = orderplacedA.price * orderplacedA.volume
    buyA = True
if orderplacedB.side == 'bid':
    totalSaleValueB =  - orderplacedB.price * orderplacedB.volume
    buyB = True
    

# Getting price books
book_A = e.get_last_price_book(instrument_A)
book_B = e.get_last_price_book(instrument_B)

# Getting the current prices
ask_price_B = book_B.asks[0].price
bid_price_B = book_B.bids[0].price
ask_price_A = book_A.asks[0].price
bid_price_A = book_A.bids[0].price

gapInB = ask_price_B - bid_price_B
gapInA = ask_price_A - bid_price_A

sellValueA_t = (ask_price_A-0.1*gapInA*)
if 

    

    
    