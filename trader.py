import krakenex
import time

fee = 0.9974

# Setting up market (Vertices) names.
a = 'XETHXXBT'
b = 'XXMRXXBT'
c = 'XLTCXXBT'
d = 'XXBTZEUR'
e = 'XXBTZUSD'
f = 'XXBTZCAD'
g = 'XXBTZJPY'
h = 'XXBTZGBP'
i = 'XETHZGBP'
j = 'XETHZJPY'
k = 'XETHZCAD'
l = 'XETHZEUR'
m = 'XETHZUSD'
n = 'XXMRZUSD'
o = 'XXMRZEUR'
p = 'XLTCZUSD'
q = 'XLTCZEUR'

# Creating API object

u = krakenex.API()
u.load_key('kraken.key')

# Holder for ticker information

tickerInfo = {a: '', b: '', c: '', d: '', e: '', f: '', g: '', h: '', i: '', j: '', k: '', l: '', m: '', n: '', o: '',
              p: '', q: ''}


# Defining function which gets/updates market information on a pair

def loadticker(tickername):
    x = u.query_public('Ticker', {'pair': tickername})
    tickerInfo[tickername] = x['result'][tickername]
    sentence = 'Ticker {} loaded'.format(tickername)
    print(sentence)


# Defining the function which buys/sells things

def maketransfer(volume, pair, price, bors):
    w = u.query_private('AddOrder',
                        {'pair': pair, 'type': bors, 'ordertype': 'limit', 'price': price, 'volume': volume})
    v = str(w['error'])
    if len(v) < 3:
        r = str(w['result']['txid'][0])
    else:
        r = v
    sentence = 'Transaction attempted: {} {} {} @ {}. \n{}'.format(bors, volume, pair, price, r)
    print(sentence)


# Defining the loops

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
                    maketransfer(x, markets[j], ticker['b'][0], 'sell')
                    x *= fee * float(ticker['b'][0])
                    print('Passing forward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)
                else:
                    x *= fee * (1 / float(ticker['a'][0]))
                    maketransfer(x, markets[j], float(ticker['a'][0]), 'buy')
                    print('Passing backward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)

        elif reversechange > 0:
            print('Market forward change is positive. Lighting up forward:')
            x = 0.002
            for j in range(2, -1, -1):
                ticker = tickerInfo[markets[j]]
                if direction[j] < 0:
                    maketransfer(x, markets[j], ticker['b'][0], 'sell')
                    x *= fee * float(ticker['b'][0])
                    print('Passing forward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)
                else:
                    x *= fee * (1 / float(ticker['a'][0]))
                    maketransfer(x, markets[j], float(ticker['a'][0]), 'buy')
                    print('Passing backward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)

        elif m_forwardchange > 0:
            print('Market forward change is positive. Lighting up forward:')
            x = 0.002
            for j in range(0, 3):
                ticker = tickerInfo[markets[j]]
                if direction[j] > 0:
                    maketransfer(x, markets[j], ticker['c'][0], 'sell')
                    x *= fee * float(ticker['c'][0])
                    print('Passing forward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)
                else:
                    x *= fee * (1 / float(ticker['c'][0]))
                    maketransfer(x, markets[j], float(ticker['c'][0]), 'buy')
                    print('Passing backward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)

        elif m_reversechange > 0:
            print('Market reverse change is positive. Lighting up reverse:')
            x = 0.002
            for j in range(2, -1, -1):
                ticker = tickerInfo[markets[j]]
                if direction[j] < 0:
                    maketransfer(x, markets[j], ticker['c'][0], 'sell')
                    x *= fee * float(ticker['c'][0])
                    print('Passing forward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)
                else:
                    x *= fee * (1 / float(ticker['c'][0]))
                    maketransfer(x, markets[j], float(ticker['c'][0]), 'buy')
                    print('Passing backward ' + str(x) + ' on ' + str(markets[j]))
                    time.sleep(2)
        else:
            time.sleep(2)
