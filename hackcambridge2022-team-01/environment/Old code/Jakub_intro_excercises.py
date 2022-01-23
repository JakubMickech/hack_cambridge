from optibook.synchronous_client import Exchange
import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')
 
print("Setup was successful.")
e = Exchange()
a = e.connect()
print("Connected to exchange.")

instrument_id = 'PHILIPS_B'

def task1():
    bookB = e.get_last_price_book(instrument_id)
    print(bookB.asks[0].price)
    result = e.insert_order(instrument_id, price=bookB.asks[0].price, volume=1, side='bid', order_type='ioc')
    print(f"Order Id: {result}")
    orders = e.get_outstanding_orders(instrument_id)
    print(orders)
    positions = e.get_positions()
    print(positions)
