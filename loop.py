def find_pair(d_graph, d_edge):
    start, dest = d_edge
    if (start, dest) in d_graph.edges:
        return start + dest, 0
    elif (dest, start) in d_graph.edges:
        return dest + start, 1
    else:
        raise ValueError('Could not find a pair which trades these assests.')

class Loop():
    def __init__(self, d_graph, assets, Tickers):
        self.graph = d_graph
        self.nodes = assets
        self.d_edges = [(assets[i-1], assets[i]) for i in range(len(assets))]
        self.trades = [find_pair(d_graph, d_edge) for d_edge in self.d_edges]
        self.pair_names = [self.trades[i][0] for i in range(len(self.trades))]
        self.Tickers = Tickers

    def simulate(self, reverse=0, prices, refresh=True):
        market = [100]
        book = [100]

        if refresh:
            self.Tickers.refresh(pairs=self.pair_names)

        trades = self.trades if not reverse else [pair[0], (pair[1] + 1) % 2 for pair in self.trades] 

        for trade in trades:
            pair = trade[0]
            ask = self.Tickers.ticker_info[pair]['a'][0]
            bid = self.Tickers.ticker_info[pair]['b'][0]
            market = self.Tickers.ticker_info[pair]['c'][0]

            if trade[1] == 0:
                book.append(book[-1] * bid * fee)
                market.append(market[-1] * market * fee)
            else:
                book.append(book[-1] * 1/ask * fee)
                market.append(market[-1] * 1/market * fee)

            return (book, market)
