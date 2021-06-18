import sys
import time
from datetime import datetime
import os

from rover import Rover
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Google Docs OAuth credential JSON file.  
GDOCS_OAUTH_JSON = os.path.join(
    os.path.dirname(__file__),
    'auth.json'
)
# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'env_data'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS  = 2


rover = Rover()

def login_open_sheet(oauth_key_file, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    try:
        scope =  ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1 # pylint: disable=redefined-outer-name
        return worksheet
    except Exception as ex: # pylint: disable=bare-except, broad-except
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, \
        and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)


print('Logging sensor measurements to\
 {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS))
print('Press Ctrl-C to quit.')
worksheet = None

device_id = rover.read_device_id()

while True:
    # Login if necessary.
    if worksheet is None:
        worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

    # Attempt to get sensor reading.
    temp = rover.sense_temperature()
    humidity = rover.sense_humidity()
    light = rover.sense_light()

    # Skip to the next reading if a valid measurement couldn't be taken.
    # This might happen if the CPU is under a lot of load and the sensor
    # can't be reliably read (timing is critical to read the sensor).


    print(f'Temperature:    {temp}')
    print(f'Humidity:       {humidity}')
    print(f'Light:          {light}')

    # Append the data in the spreadsheet, including a timestamp
    try:
        worksheet.append_row((device_id, datetime.now().isoformat(), temp, humidity, light))
    except: # pylint: disable=bare-except, broad-except
        # Error appending data, most likely because credentials are stale.
        # Null out the worksheet so a login is performed at the top of the loop.
        print('Append error, logging in again')
        worksheet = None
        time.sleep(FREQUENCY_SECONDS)
        continue

    print(f'Wrote a row to {GDOCS_SPREADSHEET_NAME}')
    time.sleep(FREQUENCY_SECONDS)

