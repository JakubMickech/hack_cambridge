import datetime
from optibook.synchronous_client import Exchange
import logging
import time
import matplotlib.pyplot as plt
import numpy as np
# Sets Logger
logger = logging.getLogger('client')
logger.setLevel('ERROR')
starttime = time.time()
print(starttime)
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
pricesBuyB = []
pricesSellA = []
pricesSellB = []
book_A = e.get_last_price_book(instrument_A)
timeStampstart = book_A.timestamp
print(e.get_positions())
i = 0
while i < 50:
    book_A = e.get_last_price_book(instrument_A)
    book_B = e.get_last_price_book(instrument_B)

    print("running")
    try:
        price_buy_A = book_A.bids[0].price
        pricesBuyA.append(price_buy_A)
        
        price_buy_B = book_B.bids[0].price
        pricesBuyB.append(price_buy_B)
        
        price_sell_A = book_B.bids[0].price
        pricesSellA.append(price_sell_A)
        
        price_sell_B = book_B.bids[0].price
        pricesSellB.append(price_sell_B)
        
        timeStamp1 = book_A.timestamp
        deltatime = timeStamp1 - timeStampstart
        deltatime = deltatime.total_seconds()
        times.append(deltatime)
        print(deltatime)
    except IndexError:
        continue
    
    time.sleep(1)
    i += 1
print(times)
print(pricesBuyA)
print(pricesBuyB)
print(pricesSellA)
print(pricesSellB)
plt.plot(times,pricesBuyA)
plt.show()