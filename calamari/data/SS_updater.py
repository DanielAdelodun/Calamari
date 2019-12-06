import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from . import info 

special_pair_names = ['XETHXXBT','XXMRXXBT','XLTCXXBT','XXBTZEUR',
                      'XXBTZUSD','XXBTZCAD','XXBTZJPY','XXBTZGBP',
                      'XETHZGBP','XETHZJPY','XETHZCAD','XETHZEUR',
                      'XETHZUSD','XXMRZUSD','XXMRZEUR','XLTCZUSD',
                      'XLTCZEUR']

class SS_Updater(object):
    """Updates a particular Google Sheet.

    Attributes:
        special_pair_names (list): A list of the Pairs to include in the spreadsheet.
        SSID (string): The ID of the spreadsheet we would like to update.
        Tickers (Updater): Default :class:`Updater` used for getting Pair data.  

    """

    def __init__(self, 
                 special_pair_names=special_pair_names,
                 SSID='1rrwAsg9Ky1oCUlSwL2kambtrE3fJzTEsS56hbqOGJuU'):
        self.special_pair_names = special_pair_names
        self.SSID = SSID
        self.Tickers = info.Updater(special_pair_names=self.special_pair_names)

        creds = None
        SCOPES = ['https://www.googleapis.com/auth/drive']

        # Check if a valid token (which is saved as 'token.pickle') is already availible, so that we do not need to log in. 
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server()
                with open('token.pickle', 'wb') as token:
                    # Save creds for next run
                    pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def update(self, Tickers=None, SSID=None, refresh=False):
        """Updates the spreadsheet.

        Args:
            Tickers (Updater): The :class:`Updater` used. Defaults to self.Tickers.
            SSID (string): ID of the spreadsheet to update. Defaults to self.SSID.
            refresh (bool): Refresh Tickers before use? 

        """
        if Tickers == None:
            Tickers = self.Tickers
        if SSID == None:
            SSID = self.SSID

        if refresh:
            Tickers.refresh()

        body = {
            "range": 'A44:AH45',
            "values": [
                      Tickers.ask_bid,
                      Tickers.market
                      ],
            "majorDimension": 'ROWS'
        }

        write_request = self.service.spreadsheets().values().update(spreadsheetId=SSID, range='A44:AH45', body=body, valueInputOption='USER_ENTERED')
        write_response = write_request.execute()
