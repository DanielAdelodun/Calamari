'''
Handles placing the orders.
'''
import krakenex 

kraken = krakenex.API()
try: 
    kraken.load_key('key.txt')
except:
    pass

def add_order(volume, pair_name, price, direction):
    direction = 'sell' if direction == 0 else 'buy' 
    result = kraken.query_private('AddOrder',
                                  {
                                    'pair': pair_name, 
                                    'type': direction, 
                                    'ordertype': 'limit',
                                    'price': price, 
                                    'volume': volume
                                  }
                                 )
    print(f"Transaction attempted: {direction} {volume} {pair_name} @ {price}.")
    print(result)
