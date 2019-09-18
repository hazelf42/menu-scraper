from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1m4D1nrUPQEZ1zXQGmRO79YO0AHjARGBMYH27h7I-ARA'

def getSheet():
    "This is google's code"
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    return sheet
            
def getFirstEmptyColumn(sheet):
    values = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range="A1:A300").execute().get('values')
    col = len(values) + 1
    return col
    
def addNewRestaurantsToSheet(sheet,firstEmptyColumn,restaurantList):
    rangeStart = "A"+str(firstEmptyColumn)
    rangeEnd = "A"+str(firstEmptyColumn)+str(len(restaurantList))
    range_name = rangeStart+":"+rangeEnd
    body = {
        'values': [restaurantList],
        'majorDimension':'COLUMNS'        
    }    
    request = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=range_name, valueInputOption='RAW', insertDataOption='OVERWRITE', body=body) 
    response = request.execute()    
    print("Updated!")


def main(restaurantList):
    sheet = getSheet()
    firstEmptyColumn = getFirstEmptyColumn(sheet)
    addNewRestaurantsToSheet(sheet,firstEmptyColumn,restaurantList)
    
    
if __name__ == '__main__':
    main(restaurantList)
