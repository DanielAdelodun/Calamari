from assets import *
import ticker_info
import networkx as nx
from pair import *
from fees import fee

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
        raise ValueError('Could not find a pair which trades these assests.')
      
class Loop():
    def __init__(self, d_graph, assets, Tickers):
        self.graph = d_graph
        self.nodes = assets
        self.d_edges = [(assets[i-1], assets[i]) for i in range(len(assets))]
        self.trades = [find_pair(d_graph, d_edge) for d_edge in self.d_edges]
        self.pair_names = [self.trades[i][0] for i in range(len(self.trades))]
        self.Tickers = Tickers

    def simulate(self, reverse=0, refresh=True):
        market = [100]
        book = [100]

        if refresh:
            self.Tickers.refresh(pairs=self.pair_names)

        trades = self.trades if not reverse else [(trade[0], (trade[1] + 1) % 2) for trade in self.trades] 

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
        
for cycle in cycles:
    loop = Loop(d_graph, cycle, Tickers) 
    print(loop.d_edges, loop.trades, sep='///')
    print(loop.simulate())
    print(loop.simulate(1))
