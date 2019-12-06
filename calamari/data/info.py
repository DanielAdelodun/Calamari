import krakenex

kraken = krakenex.API()

# We could call the 'special_pair_names' spreadsheet_pair_names instead.
# They are the Pairs (and Assets) which have a place on the google sheet.
special_pair_names = ['XETHXXBT','XXMRXXBT','XLTCXXBT','XXBTZEUR',
                 'XXBTZUSD','XXBTZCAD','XXBTZJPY','XXBTZGBP',
                 'XETHZGBP','XETHZJPY','XETHZCAD','XETHZEUR',
                 'XETHZUSD','XXMRZUSD','XXMRZEUR','XLTCZUSD',
                 'XLTCZEUR']

class Updater():
    """
    Updater objects hold information on multiple Pairs. We can update this info using the refresh() method.
    They also holds a list of 'special_pair_names'. We can format the data for these Pairs to fit on a spreadsheet.

    Attributes:
        info (dict): A dictionary contining the most up-to-date information on each Pair.
        special_pair_names (list) A list of Pair names. This defines which pairs the Updater adds to :attr:`ask_bid` and :attr:`market`.
        ask_bid (list): Alternating list of the ask/bid prices for the Pairs in :attr:`special_pair_names`.
        market (list) : Alternating list of market prices for :attr:`special_pair_names` and blank spaces.

    """
    def __init__(self, special_pair_names=special_pair_names):
        self.special_pair_names = special_pair_names
        self.info = {}
        self.ask_bid = []
        self.market = []
        self.refresh()

    def refresh(self, special=True, pairs=None):
        """
        Updates the info dictionary with fresh data from the Kraken website.
        Also updates the special lists with the same data if special is set.

        Args:
            pairs (list): List of Pair names to be refreshed.

        """
        if pairs == None:
            pairs = self.special_pair_names

        for pair in pairs: 
            try:
                returned = kraken.query_public('Ticker', {'pair':pair}) # Get ticker information for each pair in the list 'pairs'
            except:
                raise
            try:
                self.info[pair] = returned['result'][pair] # ...And put that information in a dictionary
            except:
                print('Refresh failed for:', pair)
                print(returned['error'])
                raise

        # If special is set, update special lists (alternating ask/bid prices, and market-prices/blank-space).
        if special == True:

            self.ask_bid = []
            self.market = []

            for pair in self.special_pair_names:
                self.ask_bid.append(self.info[pair]['a'][0])
                self.ask_bid.append(self.info[pair]['b'][0])
                self.market.append(self.info[pair]['c'][0])
                self.market.append(None)

    def pairs(self):
        '''
        Returns a list of the Pairs the Updater has data on
        '''
        return list(self.info)

if __name__ == "__main__":
    Tickers = Updater()
    print(Tickers.info)
