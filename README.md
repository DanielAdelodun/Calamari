These are the files for the command-line script that finds arbitrage opportunites on the [Kraken exchange.](https://www.kraken.com/en-gb/)

-------

`trader.py` is the actual trading bot - it is what executes the trades that exploit the arbitrage opportunity found.
It is currently basically the same as it was a few years ago - I will update it soon! (Hopefully...)

-------

`ticker_info.py` contains a class which can be used to build an 'Updater' object.
This object is then used to hold informfation about the different trading pairs. 
You can call `refresher_ticker()` on an Updater object to update the ticker information it holds.

-------

`SS_updater.py`, when run at the command-line, repeatedly updates the spreadsheet with recent ask/bid and market prices.

-------

`credentials.json` is the reqirued data for using the Google Sheets API - it tells google who the developer is (as opposed the user) so that you/they can track the use of the api. The user still needs to log in and give the developer access to their google account data. 

-------

`token.pickle` is where the authentication token is saved; the auth token is used to build the spreadsheet api when the user is using the app and tells the api who the user is, who the developer is, and what permissions has the user given the developer.

-------

`fees.py` contains a function used to update the fee.

-------

`assets.py` defines functions to get a list assets (currencies) and the trading pairs. 
