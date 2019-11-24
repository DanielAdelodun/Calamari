import time
import networkx
import pygraphviz

from ..data import info
from ..data.fees import *
from ..data.assets import *
from ..network.pair import *
from ..network.loop import *
from ..trade.order import *

if __name__ == "__main__":
    # Setting up Asset (node) names.
    #all_assets = get_assets()
    #special_assests = ['XXBT', 'XETH', 'XLTC', 'XXMR',
    #                   'ZUSD', 'ZCAD', 'ZEUR', 'ZGBP',
    #                   'ZJPY']

    # Pairs (edges) come pre-defined with the pair module.
    # 'special_pairs' are/will be whatever the names in 'special_pair_names' map to.
    fees.get_fee()
    special_pair_names = info.special_pair_names

    # What we will use to update the information on each trading pair/ticker.
    # Check info.py for more details.
    Tickers = info.Updater()

    # Building the network (2, actually - one directed, one undirected)
    # We can change the traders focus by changing what is in the network.
    graph  = networkx.Graph()
    d_graph = networkx.DiGraph()
    graph.add_edges_from(all_edges) # Here, we can change focus.
    d_graph.add_edges_from(all_edges) 

    path, drawing = networkx.nx_agraph.view_pygraphviz(graph, prog='neato', path='graph.png')
    # drawing = networkx.nx_agraph.to_agraph(graph)
    drawing.graph_attr.update(dpi='166', mindist=3, overlap='False', splines='ortho')
    drawing.draw('drawing.png', 'png', 'neato')
    drawing.draw('drawdot.png', 'png', 'dot')

    # Finding the Loops in that network
    cycles = networkx.cycle_basis(graph, 'XXBT')
    loops = [Loop(d_graph, cycle, Tickers) for cycle in cycles]

    # Finally, we can find profitable Loops and exploit them.
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

