from .pair import *
from ..trade.order import *
from ..data.assets import *
from ..data.fees import fee
from ..data.info import *
import networkx as nx

class Loop():
    def __init__(self, d_graph, assets, Tickers):
        self.graph = d_graph
        self.nodes = assets
        self.d_edges = [(assets[i-1], assets[i]) for i in range(len(assets))]
        self.trades = [self.find_pair(d_edge, d_graph) for d_edge in self.d_edges]
        self.pair_names = [self.trades[i][0] for i in range(len(self.trades))]
        self.Tickers = Tickers

    def find_pair(self, d_edge, d_graph=None):
        '''
        Given a directed edge, return a vaild Pair name if one exists, 
        indicating the direction of the Pair relatative to the directed edge
        '''
        if d_graph == None:
            d_graph = self.graph
        start, dest = d_edge
        if (start, dest) in d_graph.edges:
            return start + dest, 0
        elif (dest, start) in d_graph.edges:
            return dest + start, 1
        else:
            raise ValueError('Could not find a pair which trades these assets.')

    def calculate(self, reverse=False, refresh=True, volume=100, silent=False):
        market = [volume]
        book = [volume]

        trades = self.trades if not reverse else [(trade[0], (trade[1] + 1) % 2) for trade in self.trades] 
        if reverse:
            trades.reverse()
        if refresh:
            self.Tickers.refresh(pairs=self.pair_names)
        if not silent:
            print('\nCalculating the volume changes for the following trades: ')
            for trade in trades[:-1]:
                print(trade, '---->')
            print(trades[-1], '\n--------')

        for trade in trades:
            pair = trade[0]
            ask = float(self.Tickers.info[pair]['a'][0])
            bid = float(self.Tickers.info[pair]['b'][0])
            marketp = float(self.Tickers.info[pair]['c'][0])

            if trade[1] == 0:
                book.append(book[-1] * bid * fee)
                market.append(market[-1] * marketp * fee)
            else:
                book.append(book[-1] * 1/ask * fee)
                market.append(market[-1] * 1/marketp * fee)
        if not silent:
            print('Volume changes after each transaction using...')
            print(' * Book Prices: ', book)
            print(' * Market Prices: ', market)
            print('========\n')
        return (book, market)

    def execute(self, start_volume, reverse=False, refresh=False, market=False, silent=True):
        volumes = self.calculate(reverse, 
                                 refresh,
                                 start_volume,
                                 silent)[1] if market \
             else self.calculate(reverse,
                                 refresh, 
                                 start_volume, 
                                 silent)[0]

        trades = [(trade[0], (trade[1] + 1) % 2) for trade in self.trades] if reverse else self.trades
       
        if reverse:
            trades.reverse()
        if refresh:
            self.Tickers.refresh(pairs=self.pair_names)
    
        i = 0
        for trade in trades:
            pair = trade[0]
            ask = float(self.Tickers.info[pair]['a'][0])
            bid = float(self.Tickers.info[pair]['b'][0])
            marketp = float(self.Tickers.info[pair]['c'][0])

            volume = volumes[i+1] if trade[1] else volumes[i]
            price = marketp if market else (ask if trade[1] else bid)

            add_order(volume, pair, price, trade[1])
            i += 1

#if __name__ == '__main__':
Tickers = Updater()

graph = nx.Graph()
d_graph = nx.DiGraph()

graph.add_edges_from(all_edges)
d_graph.add_edges_from(all_edges)

cycles = nx.cycle_basis(graph, 'XXBT')
loops = []

for cycle in cycles[0:5]:
    loop = Loop(d_graph, cycle, Tickers) 
    loops.append(loop)
    loop.execute(1, 0, refresh=True, silent=False)
    loop.execute(1, 1, refresh=True, silent=False)
    print([loop.nodes for loop in loops])
