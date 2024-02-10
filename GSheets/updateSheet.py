import os.path
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build,Resource
from googleapiclient.errors import HttpError

from classes.partnerData import Partner
from utils.stringUtils import stringArrayToStr

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SAMPLE_SPREADSHEET_ID = "1deXQhe0oIKTty-jbkSqYcQjqBhPG7Bhrsyq-TBX3SVo"
SAMPLE_RANGE_NAME = "A2:H"


def writeNewData(partners:List[Partner]):
  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
      
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service:Resource = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Clear all data from sheet
    # sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    
    # Insert new data
    for partner in partners:
      # specString=""
      # for specInd,spec in enumerate(partner.specializations):
      #   specString+=spec
      #   if((specInd+1)<len(partner.specializations)):specString+=","
      sheet.values().append(valueInputOption="RAW",spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,body={"majorDimension":"ROWS","range":SAMPLE_RANGE_NAME,"values":[[partner.name,partner.source,partner.contactDetails.web,stringArrayToStr(partner.specializations),partner.source,stringArrayToStr(partner.locations),partner.contactDetails.email,partner.contactDetails.phone]]}).execute()

  except HttpError as err:
    print(err)
