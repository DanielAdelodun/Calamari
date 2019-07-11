import time
import krakenex
import networkx
import ticker_info
import fees.fee as fee
from pair import *
from assets import *

kraken = krakenex.API()
kraken.load_key('kraken.key')

# Setting up asset (vertex) names.
all_assets = get_assets()
special_assests = ['XXBT', 'XETH', 'XLTC', 'XXMR', 'ZUSD', 'ZCAD', 'ZEUR', 'ZGBP', 'ZJPY']

# Edges should come pre-defined with pair. The 'special_edges' are whatever the names in 'special_pair_names' map to.
special_pair_names = ticker_info.special_pairs

# This will be what we will use to update the information on each trading pair/ticker.
# Check ticker_info.py for more details.
Tickers = ticker_info.Updater()

# Defining the function which buys/sells things
def add_order(volume, pair_name, price, direction):
    result = kraken.query_private('AddOrder',
                                  {
                                    'pair': pair, 
                                    'type': direction, 
                                    'ordertype': 'limit',
                                    'price': price, 
                                    'volume': volume
                                  }
                                 )
    print('Transaction attempted: {direction} {volume} {pair} @ {price}.')
    print(result)


# Building the network
network = networkx.Graph()
all_edges = [all_pairs[pair].edge for pair in all_pairs]
network.add_edges_from(all_edges)
cycles = networkx.cycle_basis(network,' XXBT')

loops = [[[a, -1], [i, 1], [h, -1]], [[a, -1], [j, 1], [g, -1]], [[a, -1], [k, 1], [f, -1]], [[a, -1], [m, 1], [e, -1]],
         [[a, -1], [l, 1], [d, -1]], [[c, -1], [q, 1], [d, -1]], [[c, -1], [p, 1], [e, -1]], [[b, -1], [o, 1], [d, -1]],
         [[b, -1], [n, 1], [e, -1]]]


# Creating loop objects

class LoopOfThree:
    def __init__(self, vectors):
        self.markets = [vectors[0][0], vectors[1][0], vectors[2][0]]
        self.direction = [vectors[0][1], vectors[1][1], vectors[2][1]]
        for x in self.markets:
            loadticker(x)

    def updateinfo(self):
        for x in self.markets:
            loadticker(x)

    def forwardchange(self, x=100):
        markets = self.markets
        direction = self.direction
        for y in range(0, 3):
            direct = direction[y]
            if direct < 0:
                x *= (fee * 1 / (float(tickerInfo[markets[y]]['a'][0])))
            else:
                x *= (fee * float(tickerInfo[markets[y]]['b'][0]))
        return x

    def reversechange(self, x=100):
        markets = self.markets
        direction = self.direction
        for y in range(0, 3):
            direct = direction[2 - y]
            if direct > 0:
                x *= (fee * 1 / (float(tickerInfo[markets[2 - y]]['a'][0])))
            else:
                x *= (fee * float(tickerInfo[markets[2 - y]]['b'][0]))
        return x

    def m_forwardchange(self, x=100):
        markets = self.markets
        direction = self.direction
        for y in range(0, 3):
            direct = direction[y]
            if direct < 0:
                x *= (fee * 1 / (float(tickerInfo[markets[y]]['c'][0])))
            else:
                x *= (fee * float(tickerInfo[markets[y]]['c'][0]))
        return x

    def m_reversechange(self, x=100):
        markets = self.markets
        direction = self.direction
        for y in range(0, 3):
            direct = direction[2 - y]
            if direct > 0:
                x *= (fee * 1 / (float(tickerInfo[markets[2 - y]]['c'][0])))
            else:
                x *= (fee * float(tickerInfo[markets[2 - y]]['c'][0]))
        return x


for t in range(0, 50):
    for y in range(0, 9):
        print('\n')
        new2 = LoopOfThree(loops[y])
        forwardchange = new2.forwardchange() - 100
        reversechange = new2.reversechange() - 100
        m_forwardchange = new2.m_forwardchange() - 100
        m_reversechange = new2.m_reversechange() - 100
        direction = new2.direction
        markets = new2.markets

        print('Forward change is ' + str(forwardchange))
        print('Reverse change is ' + str(reversechange))
        print('Market forward change is ' + str(m_forwardchange))
        print('Market reverse change is ' + str(m_reversechange))

        if forwardchange > 0:
            print('Forward change is positive. Lighting up forward:')
            x = 0.002
            for j in range(0, 3):
                ticker = tickerInfo[markets[j]]
                if direction[j] > 0:
                    add_order(x, markets[j], ticker['b'][0], 'sell')
                    x *= fee * float(ticker['b'][0])
                    print('Passing forward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)
                else:
                    x *= fee * (1 / float(ticker['a'][0]))
                    add_order(x, markets[j], float(ticker['a'][0]), 'buy')
                    print('Passing backward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)

        elif reversechange > 0:
            print('Market forward change is positive. Lighting up forward:')
            x = 0.002
            for j in range(2, -1, -1):
                ticker = tickerInfo[markets[j]]
                if direction[j] < 0:
                    add_order(x, markets[j], ticker['b'][0], 'sell')
                    x *= fee * float(ticker['b'][0])
                    print('Passing forward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)
                else:
                    x *= fee * (1 / float(ticker['a'][0]))
                    add_order(x, markets[j], float(ticker['a'][0]), 'buy')
                    print('Passing backward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)

        elif m_forwardchange > 0:
            print('Market forward change is positive. Lighting up forward:')
            x = 0.002
            for j in range(0, 3):
                ticker = tickerInfo[markets[j]]
                if direction[j] > 0:
                    add_order(x, markets[j], ticker['c'][0], 'sell')
                    x *= fee * float(ticker['c'][0])
                    print('Passing forward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)
                else:
                    x *= fee * (1 / float(ticker['c'][0]))
                    add_order(x, markets[j], float(ticker['c'][0]), 'buy')
                    print('Passing backward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)

        elif m_reversechange > 0:
            print('Market reverse change is positive. Lighting up reverse:')
            x = 0.002
            for j in range(2, -1, -1):
                ticker = tickerInfo[markets[j]]
                if direction[j] < 0:
                    add_order(x, markets[j], ticker['c'][0], 'sell')
                    x *= fee * float(ticker['c'][0])
                    print('Passing forward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)
                else:
                    x *= fee * (1 / float(ticker['c'][0]))
                    add_order(x, markets[j], float(ticker['c'][0]), 'buy')
                    print('Passing backward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)
        else:
            time.sleep(2)
