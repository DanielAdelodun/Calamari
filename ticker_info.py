import krakenex
import json

kraken = krakenex.API()
pairs = ['XETHXXBT','XXMRXXBT','XLTCXXBT','XXBTZEUR','XXBTZUSD','XXBTZCAD','XXBTZJPY','XXBTZGBP','XETHZGBP','XETHZJPY','XETHZCAD','XETHZEUR','XETHZUSD','XXMRZUSD','XXMRZEUR','XLTCZUSD','XLTCZEUR']

# Dictionary of ticker information
ticker_info = {}

# Ticker information formatted in a specific way, so that I can I easily upload the valuse to a spreadsheet.
# List of alternating ask/bid prices of different pairs.
ticker_ab = []
# List of market prices, seperated by a blank space (None).
ticker_m = []

def refresh_tickers(set=False, pairs=pairs):
        '''
        Updates the ticker_info dictionary with fresh data from the Kraken website.
        Also updates the special lists with the same data.
        TODO If set=True, then special list should be untouched, and only the pairs in the parameter should be updated in the dictionary.
        '''
        global ticker_ab, ticker_m

        ticker_ab = []
        ticker_m = []

        for x in pairs: 
                # Using the Krakenex API client, get ticker information for each pair in the list 'pairs'...
                returned = kraken.query_public('Ticker', {'pair':x})
                # ...And put that information in a dictionary, with the matching pair name as the key.
                ticker_info[x] = returned['result'][x]
                # Also, append to lists of alternating ask/bid prices the ask/bid, and to the list of market prices the market price (followed by a blank space).
                a = returned['result'][x]['a'][0]
                b = returned['result'][x]['b'][0]
                m = returned['result'][x]['c'][0]
                ticker_ab.append(a)
                ticker_ab.append(b)
                ticker_m.append(m)
                ticker_m.append(None)

        if __name__ == "__main__":
                print(ticker_ab, ticker_m, sep='\n')

refresh_tickers()
if __name__ == "__main__":
        print(ticker_info)
        print(len(ticker_ab), len(ticker_m))
