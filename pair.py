from assets import *

# Setting up market (edges) and their names to be a simple class.
all_pairs_info = get_asset_pairs()

class Pair():
    def __init__(self, name):
        self.name = name
        self.info = all_pairs_info[name]
        self.quote = all_pairs_info[name]['quote']
        self.base = all_pairs_info[name]['base']
        self.edge = (all_pairs_info[name]['base'], all_pairs_info[name]['quote'])

all_pair_names = [pair_name for pair_name in all_pairs_info]
all_pairs = {}
for pair_name in all_pair_names:
    all_pairs[pair_name] = Pair(pair_name)
