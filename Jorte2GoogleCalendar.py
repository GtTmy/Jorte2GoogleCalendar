from __future__ import print_function
import httplib2
import os

import csv

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Jorte2GoogleCalendar'

# Write your carender ID
CARENDAR_ID = ''

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'Jorte2GoogleCalendar_credential.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """read schedule_data.csv and insert all events to google calendar
    """

    # OAuth
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # read csv
    with open('schedule_data.csv', 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        next(csv_reader) # skip header
        for data in csv_reader:
            date_number = [ int(el) for el in data[0].split('/') ]
            date_start = datetime.date(date_number[0], date_number[1], date_number[2])
            date_number = [ int(el) for el in data[1].split('/') ]
            date_end = datetime.date(date_number[0], date_number[1], date_number[2])
            time_start = data[2]
            time_end = data[3]

            print(str(date_start) + '...' + data[4] + ' is inserting.')

            if time_start == '' and time_end == '': # all day event
                if date_start != date_end:
                    date_end = date_end + datetime.timedelta(days=1)
                event = {
                    'start':{'date':str(date_start)},
                    'end':{'date':str(date_end)},
                    'summary':data[4],
                    'description':data[11],
                    'location':data[12]
                    }
            else: # (normal) event
                dateTime_start = str(date_start) + 'T' + (time_start if time_start!='' else time_end) + ':00+09:00'
                dateTime_end = str(date_end) + 'T' + (time_end if time_end!='' else time_start) + ':00+09:00'
                event = {
                    'start':{'dateTime':dateTime_start},
                    'end':{'dateTime':dateTime_end},
                    'summary':data[4],
                    'description':data[11],
                    'location':data[12]
                    }

            target_calendar_id = CARENDAR_ID if CARENDAR_ID!='' else 'primary'
            service.events().insert(
                calendarId=target_calendar_id, body=event
            ).execute()

        print('Done!')

if __name__ == '__main__':
    main()