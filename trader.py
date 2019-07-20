import time
import krakenex
import networkx
import ticker_info
from fees import *
from pair import *
from loop import *
from order import *
from assets import *

kraken = krakenex.API()
kraken.load_key('key.txt')

# Setting up asset (node) names.
all_assets = get_assets()
special_assests = ['XXBT', 'XETH', 'XLTC', 'XXMR', 'ZUSD', 'ZCAD', 'ZEUR', 'ZGBP', 'ZJPY']

# Pairs/edges should come pre-defined with pair. The 'special_pairs' are whatever the names in 'special_pair_names' map to.
special_pair_names = ticker_info.special_pairs

# This will be what we will use to update the information on each trading pair/ticker.
# Check ticker_info.py for more details.
Tickers = ticker_info.Updater()

# Building the network (2, actually - one directed, one undirected)
graph  = networkx.Graph()
d_graph = networkx.DiGraph()
graph.add_edges_from(all_edges)
d_graph.add_edges_from(all_edges)

# Finding the loops in that network
cycles = networkx.cycle_basis(graph, 'XXBT')
loops = [Loop(d_graph, cycle, Tickers) for cycle in cycles]

# Finally, we can find profitable loops and then trade them
for loop in loops:

    # Check forward direction.
    volumes = loop.calculate()
    if volumes[0][0] < volumes[0][-1]: # Checking if the volume of bitcoin at the end would be larger than at the start.
        loop.execute(0.01)
        continue
    elif volumes[1][0] < volumes[1][-1]: # Ditto, but using market prices.
        loop.execute(0.01, market=True)
        continue

    # Check reverse.
    volumes = loop.calculate(reverse=True)
    if volumes[0][0] < volumes[0][-1]:
        loop.execute(0.01, reverse=True)
        continue
    elif volumes[1][0] < volumes[1][-1]:
        loop.execute(0.01, reverse=True, market=True)
        continue

