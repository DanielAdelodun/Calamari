from .data.fees import *
from .data.info import *
from .data.SS_updater import *
from .network.loop import *
from .trade.trader import *
from time import sleep
import networkx as nx

Tickers = Updater()
supdater = SS_Updater()

graph = nx.Graph()
d_graph = nx.DiGraph()

graph.add_edges_from(all_edges)
d_graph.add_edges_from(all_edges)

cycles = nx.cycle_basis(graph, 'XXBT')
loops = [Loop(d_graph, cycle, Tickers) for cycle in cycles]

drawing = nx.nx_agraph.to_agraph(graph)

def draw():
    drawing.write('visuals/drawing.dot')
    drawing.graph_attr.update(dpi='166', mindist=3, overlap='False', splines='ortho')
    drawing.draw('visuals/drawneato.png', 'png', 'neato')
    drawing.draw('visuals/drawdot.png', 'png', 'dot')

def start():
    draw()
    get_fee()
    
    while(True):
        try:
            supdater.update(refresh=True)
            print('\n----\nSpreadsheet updated.\n')
        except:
            print('Error updating spreadsheet')
            continue
        for loop in loops:
            try:
                trader(loop)
                continue
            except KeyboardInterrupt:
                raise
            except Exception as ex:
                print("Something went wrong: ", ex)
                sleep(0.5)
                continue
            # Add updates to graph
