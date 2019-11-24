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
        Ticker (Updater): Default :class:`Updater` used for getting Pair data.  

    """

    def __init__(self, 
                 special_pair_names=special_pair_names,
                 SSID='1rrwAsg9Ky1oCUlSwL2kambtrE3fJzTEsS56hbqOGJuU'):
        self.special_pair_names = special_pair_names
        self.SSID = SSID
        self.Ticker = info.Updater(special_pair_names=self.special_pair_names)

    def update(self, Ticker=None, SSID=None, refresh=False):
        """Updates the spreadsheet.

        Args:
            Ticker (Updater): The :class:`Updater` used. Defaults to self.Ticker.
            SSID (string): ID of the spreadsheet to update. Defaults to self.SSID.
            refresh (bool): Refresh Ticker before use? 

        """
        if Ticker == None:
            Ticker = self.Ticker
            refresh = True
        SCOPES = ['https://www.googleapis.com/auth/drive']
        if SSID == None:
            SSID = self.SSID

        if refresh:
            Ticker.refresh()

        body = {
            "range": 'A44:AH45',
            "values": [
                      Ticker.ask_bid,
                      Ticker.market
                      ],
            "majorDimension": 'ROWS'
        }

        creds = None

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

        service = build('sheets', 'v4', credentials=creds)
        write_request = service.spreadsheets().values().update(spreadsheetId=SSID, range='A44:AH45', body=body, valueInputOption='USER_ENTERED')
        write_response = write_request.execute()
        read_request = service.spreadsheets().values().get(spreadsheetId=SSID, range='D21:I41', majorDimension='ROWS')
        read_response = read_request.execute()
        print(read_request)
        print(read_response['values'])
        print(write_request)
        print(write_response)
