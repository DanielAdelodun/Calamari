import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import ticker_info 

pairs = ['XETHXXBT','XXMRXXBT','XLTCXXBT','XXBTZEUR','XXBTZUSD','XXBTZCAD','XXBTZJPY','XXBTZGBP','XETHZGBP','XETHZJPY','XETHZCAD','XETHZEUR','XETHZUSD','XXMRZUSD','XXMRZEUR','XLTCZUSD','XLTCZEUR']


while True:
    ticker_info.refresh_tickers(pairs=pairs)
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SSID = '1rrwAsg9Ky1oCUlSwL2kambtrE3fJzTEsS56hbqOGJuU'

    body = {
        "range": 'A44:AH45',
        "values": [
                  ticker_info.ticker_ab,
                  ticker_info.ticker_m
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
