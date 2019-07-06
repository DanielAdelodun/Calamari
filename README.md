These are the files for the command-line script that finds arbitrage
opportunites on the Kraken exchange.

-------
-------

ticker_info.py contains the variables ticker_ab and ticker_m.
It also contains the method ticker_refresh()

- ticker_ab is a list of alternating the ask-bid prices
- ticker_m is a list of alternating market prices and blank spaces.

These will become rows 44 and 45 in the spreadsheet: hence the formatting.

- ticker_refresh() is used to update these lists.

ticker_refresh() uses the krakenex module to get data directly from the
Kraken website, and then puts that data in ticker_info, ticker_ab, and
ticker_m

-------

SS_updater.py when run at the command-line updates the spreadsheet the
ask/bid and market prices.

-------

credentials.json is the reqirued data for using the google sheets API - 
it tells google who the developer is (as opposed the user) so that you/they
can track the use of the api. The user still needs to log in and give the 
developer access to their google account data. 

-------

token.pickle is where the authetification token is saved; the auth token is
used to build the spreadsheet api when the user is using the app and tells 
the api who the user is, who the developer is, and what permissions has the
user given the developer.
