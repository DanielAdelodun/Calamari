from ..data.assets import *

all_pair_info = get_asset_pairs()

class Pair():
    '''
    Pairs contain information on the base asset and the quote asset. 
    From this, we know the direction of the edge in the network.
    '''
    def __init__(self, name, pair_info=all_pair_info):
        self.name = name
        self.info = pair_info[name]
        self.quote = pair_info[name]['quote']
        self.base = pair_info[name]['base']
        self.edge = (pair_info[name]['base'], pair_info[name]['quote'])

all_pairs = {}
all_pair_names = [pair_name for pair_name in all_pair_info]
for pair_name in all_pair_names:
    all_pairs[pair_name] = Pair(pair_name)

all_edges = [all_pairs[pair].edge for pair in all_pairs]

