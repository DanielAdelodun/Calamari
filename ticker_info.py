import krakenex

kraken = krakenex.API()
special_pairs = ['XETHXXBT','XXMRXXBT','XLTCXXBT','XXBTZEUR',
                 'XXBTZUSD','XXBTZCAD','XXBTZJPY','XXBTZGBP',
                 'XETHZGBP','XETHZJPY','XETHZCAD','XETHZEUR',
                 'XETHZUSD','XXMRZUSD','XXMRZEUR','XLTCZUSD',
                 'XLTCZEUR']

class Updater():
    '''
    An instance of updater provides a holder for information on different pairs, as well as a way to update these pairs.
    It also defines a list of 'special pairs' and gives a way to easily access the data for these pairs.

    '''
    def __init__(self, special_pairs=special_pairs):
        self.special_pairs = special_pairs
        self.ticker_info = {}
        self.ask_bid = []
        self.market = []
        self.refresh()

    def refresh(self, special=True, pairs=None):
        '''
        Updates the ticker_info dictionary with fresh data from the Kraken website.
        Also updates the special lists with the same data if special is set.
        '''
        if pairs == None:
            pairs = self.special_pairs

        for pair in pairs: 
            returned = kraken.query_public('Ticker', {'pair':pair}) # Using the Krakenex API client, get ticker information for each pair in the list 'pairs'...
            self.ticker_info[pair] = returned['result'][pair] # ...And put that information in a dictionary, with the matching pair name as the key.

        # if special is set, also update special lists (alternating ask/bid prices, and market prices (followed by a blank space).
        if special == True:

            self.ask_bid = []
            self.market = []

            for pair in special_pairs:
                self.ask_bid.append(self.ticker_info[pair]['a'][0])
                self.ask_bid.append(self.ticker_info[pair]['b'][0])
                self.market.append(self.ticker_info[pair]['c'][0])
                self.market.append(None)

    def pairs(self):
        return list(self.ticker_info)

if __name__ == "__main__":
    Tickers = Updater()
    print(Tickers.ticker_info)
