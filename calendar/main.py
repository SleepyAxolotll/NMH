import os
import json
import pickle
import datetime
from fastapi import FastAPI, Query, HTTPException
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from fastapi.responses import FileResponse, JSONResponse
from openpyxl import Workbook

app = FastAPI()
SAVE_DIRECTORY = "excel_files"
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Function to get credentials from environment variable
def get_credentials():
    credentials_json = os.getenv('calcreds')
    if credentials_json is None:
        raise HTTPException(status_code=500, detail="Google OAuth credentials not found in environment variables.")
    
    credentials_info = json.loads(credentials_json)
    flow = InstalledAppFlow.from_client_config(credentials_info, SCOPES)
    
    # Check if token.pkl exists
    token_path = 'token.pkl'
    if os.path.exists(token_path):
        credentials = pickle.load(open(token_path, 'rb'))
    else:
        credentials = flow.run_local_server(port=0)
        pickle.dump(credentials, open(token_path, 'wb'))

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        pickle.dump(credentials, open(token_path, 'wb'))

    return credentials

@app.get("/get_calendar")
def get_calendar(start_date: str = Query(...), num_events: int = Query(10)):
    try:
        if not os.path.exists(SAVE_DIRECTORY):
            os.makedirs(SAVE_DIRECTORY)
        excel_file_path = os.path.join(SAVE_DIRECTORY, "calendar_events.xlsx")
       
        credentials = get_credentials()
        service = build("calendar", "v3", credentials=credentials)

        # Set custom start date
        custom_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").isoformat() + 'Z'

        # Create a new Workbook
        wb = Workbook()
        ws = wb.active
        ws.append(['Date', 'Activity Type', 'Event'])

        # List all calendars associated with the user
        calendars_result = service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])
    
        # Iterate through each calendar to retrieve events
        for calendar in calendars:
            calendar_id = calendar['id']
            summary = calendar['summary']
            if calendar.get('primary', False):
                continue

            # Retrieve events for the calendar using its calendarId
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=custom_start_date,
                maxResults=num_events,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])
            if not events:
                print(f"No upcoming events found for {summary}")
            else:
                print(f"Upcoming events for {summary}:")
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    event_summary = event['summary']

                    # Determine the activity_type based on the calendar summary
                    if summary == "webcal://nmhschool.myschoolapp.com/podium/feed/iCal.aspx?z=K9ml5CeS9MkMNKGT2fTU5TJnUKTWzlMy%2bEXk0mQ61dycM%2bfBbBWb3Fhkdwxaa7jNRBAq%2bkSB%2fSXMYtk2r2zM3Q%3d%3d":
                        activity_type = "School Calendar"
                    elif summary == "webcal://nmhschool.myschoolapp.com/podium/feed/iCal.aspx?z=K9ml5CeS9MkMNKGT2fTU5TJnUKTWzlMy%2bEXk0mQ61dygGzRo1jN9r7CbCE6hV1MrBwIX06vrlLhG1MnO%2bE%2fIYA%3d%3d":
                        activity_type = "Athletics"
                    else:
                        activity_type = "Arts"

                    if 'T' in start:
                        start_time = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
                        formatted_start_time = start_time.strftime("%Y-%m-%d %I:%M %p")
                    else:
                        start_time = datetime.datetime.strptime(start, "%Y-%m-%d")
                        formatted_start_time = start_time.strftime("%Y-%m-%d")

                    ws.append([formatted_start_time, activity_type, event_summary])

        wb.save(excel_file_path)
        return FileResponse(excel_file_path, filename='calendar_events.xlsx', media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})
