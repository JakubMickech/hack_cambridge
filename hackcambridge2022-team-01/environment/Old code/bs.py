from optibook.synchronous_client import Exchange
import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful.")
instrument_id = 'PHILIPS_A'

e = Exchange()
a = e.connect()
buySellRatioA = 0
buySellRatioB = 0
positions = e.get_positions()
for p in positions:
    print(p, positions[p])

print(positions)

buySellRatioA = positions["PHILIPS_A"] / 10  * 1.03
buySellRatioB = positions["PHILIPS_B"] / 10  * 1.03 
    
print(buySellRatioA)
print(buySellRatioB)

#alphaABuy = errorMargin*()