##
# THIS IS EXTERNAL CODE
##


import pickle
import os.path
import config
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

  
# Define the SCOPES. If modifying it,
# delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/drive']
  
  
  
# Create a function getFileList with 
# parameter N which is the length of 
# the list of files.
def getFileList(N):
    print("Getting files...")
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None
  
    # The file token.pickle stores the 
    # user's access and refresh tokens. It is
    # created automatically when the authorization 
    # flow completes for the first time.
  
    # Check if file token.pickle exists
    if os.path.exists('token.pickle'):
  
        # Read the token from the file and 
        # store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
  
    # If no valid credentials are available, 
    # request the user to log in.
    if not creds or not creds.valid:
  
        # If token is expired, it will be refreshed,
        # else, we will request a new one.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
  
        # Save the access token in token.pickle 
        # file for future usage
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
  
    # Connect to the API service
    service = build('drive', 'v3', credentials=creds)
  
    # request a list of first N files or 
    # folders with name and id from the API.
    resource = service.files()
    result = resource.list(pageSize=N, fields="files(id, name)").execute()
  
    # return the result dictionary containing 
    # the information about the files
    return result

result_dict = getFileList(config.MAX_FOLDERS_DEEPNES)
  

def ls():
  print("searching files....")
  files = result_dict.get('files')
  print(f"done, {len(files)} founded")
  return files
  
  





