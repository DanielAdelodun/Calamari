from assets import *
import ticker_info
import networkx as nx
from pair import *
from fees import fee
from order import *

Tickers = ticker_info.Updater()

graph = nx.Graph()
d_graph = nx.DiGraph()

graph.add_edges_from(all_edges)
d_graph.add_edges_from(all_edges)

cycles = nx.cycle_basis(graph, 'XXBT')

def find_pair(d_graph, d_edge):
    start, dest = d_edge
    if (start, dest) in d_graph.edges:
        return start + dest, 0
    elif (dest, start) in d_graph.edges:
        return dest + start, 1
    else:
        raise ValueError('Could not find a pair which trades these assets.')
      
class Loop():
    def __init__(self, d_graph, assets, Tickers):
        self.graph = d_graph
        self.nodes = assets
        self.d_edges = [(assets[i-1], assets[i]) for i in range(len(assets))]
        self.trades = [find_pair(d_graph, d_edge) for d_edge in self.d_edges]
        self.pair_names = [self.trades[i][0] for i in range(len(self.trades))]
        self.Tickers = Tickers

    def calculate(self, reverse=False, refresh=True, volume=100):
        market = [volume]
        book = [volume]

        trades = self.trades if not reverse else [(trade[0], (trade[1] + 1) % 2) for trade in self.trades] 
        if reverse:
            trades.reverse()
        if refresh:
            self.Tickers.refresh(pairs=self.pair_names)
        print(trades)

        for trade in trades:
            pair = trade[0]
            ask = float(self.Tickers.ticker_info[pair]['a'][0])
            bid = float(self.Tickers.ticker_info[pair]['b'][0])
            marketp = float(self.Tickers.ticker_info[pair]['c'][0])

            if trade[1] == 0:
                book.append(book[-1] * bid * fee)
                market.append(market[-1] * marketp * fee)
            else:
                book.append(book[-1] * 1/ask * fee)
                market.append(market[-1] * 1/marketp * fee)

        return (book, market)

    def execute(self, start_volume, reverse=False, refresh=False, market=False):
        i = 0
        volumes = self.calculate(reverse, refresh, start_volume)[1] if market else self.calculate(reverse, refresh, start_volume)[0]
        trades = [(trade[0], (trade[1] + 1) % 2) for trade in self.trades] if reverse else self.trades
        if reverse:
            trades.reverse()
        if refresh:
            self.Tickers.refresh(pairs=self.pair_names)
    
        for trade in trades:
            
            pair = trade[0]
            ask = float(self.Tickers.ticker_info[pair]['a'][0])
            bid = float(self.Tickers.ticker_info[pair]['b'][0])
            marketp = float(self.Tickers.ticker_info[pair]['c'][0])

            volume = volumes[i+1] if trade[1] else volumes[i]
            price = marketp if market else (ask if trade[1] else bid)

            add_order(volume, trade[0], price, trade[1])
            i += 1

for cycle in cycles:
    loop = Loop(d_graph, cycle, Tickers) 
    print(loop.d_edges, loop.trades, sep='///')
    print(loop.calculate())
    print(loop.calculate(1))
    loop.execute(1, 0)
    loop.execute(1, 1)
