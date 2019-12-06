These are the files for the command-line script that finds arbitrage opportunites on the [Kraken exchange.](https://www.kraken.com/en-gb/)

-------

`trader` is the actual trading bot - it looks at loops, and finds trading opportunites within them.

-------

`info` contains a class which can be used to build an 'Updater' object.
This object is then used to hold informfation about the different trading pairs. 
You can call `refresh()` on an Updater object to update the ticker information it holds.

-------

`SS_updater`, Updates the spreadsheet with recent ask/bid and market prices.

-------

`fees` contains a function used to update the fee.

-------

`assets` defines functions to get a list assets (currencies) and the trading pairs.

-------

`pair` defines a class `Pair`. An instance of `Pair` will contain information about a specific trading pair - it is used mostly in creating edges for the network.

-------

`loop` contains the Loop class definitions. Loop objects know what assests are in the loop, how to trade in a circle around the loop, and the exchange rates between all the relevant pairs
