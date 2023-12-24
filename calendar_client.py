# установка нужных библиотек
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# файл creds.json должен находиться в той же папке, что и этот файл

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
# id календаря (можно менять)
calendar = '69eb71a19c867c73a340ea9ed121076e55ed30c8681a470d3af11680c766b98d@group.calendar.google.com'


# дату надо именно в таком формате ГГГГ-ММ-ДД (дата end не включительно)
def add_event_to_gcal(calendarid=calendar, title='Просмотр лекции', desc='посмотреть лекцию', start='2023-12-25', end='2023-12-26'):

    event = {
        'summary': title,
        'description': desc,
        'start': {
            'date': start,
        },
        'end': {
            'date': end,
        }
    }

    obj.add_event(calendar_id=calendarid, body=event)

    return

# примеры использования
add_event_to_gcal()
# add_event_to_gcal(title='check',desc='ghjdthrf')

# почта, которой нужно разрешить доступ
# lecturebot@lecturebot.iam.gserviceaccount.com


