# установка нужных библиотек
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# файл creds.json должен находиться в той же папке, что и этот файл

import pprint
from google.oauth2 import service_account
from googleapiclient import discovery


class GoogleCalendar:
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    FILE_PATH = 'creds.json'

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            filename=self.FILE_PATH, scopes=self.SCOPES
        )
        self.service = discovery.build('calendar', 'v3', credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()  # list of calendars

    def add_calendar(self, calendar_id):
        calendar_list_entry = {
            'id': calendar_id
        }

        return self.service.calendarList().insert(body=calendar_list_entry).execute()

    def add_event(self, calendar_id, body):
        return self.service.events().insert(
            calendarId=calendar_id,
            body=body).execute()


obj = GoogleCalendar()
calendar = '69eb71a19c867c73a340ea9ed121076e55ed30c8681a470d3af11680c766b98d@group.calendar.google.com'

# pprint.pprint(obj.get_calendar_list())   # list of calendars

event = {
    'summary': 'Тестовое название',
    'location': 'Москва',
    'description': 'Тестовое описание',
    'start': {
        'date': '2023-12-11',
    },
    'end': {
        'date': '2023-12-13',
    }
}

event = obj.add_event(calendar_id=calendar, body=event)
