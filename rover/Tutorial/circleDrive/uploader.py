import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

class Uploader:

    def __init__(self):
        super(Uploader, self).__init__()

        self.sheet_name = os.getenv('SPREADSHEET_NAME')

        self.columns = self.read_columns()

        self.scope = self.create_scope()

        self.credentials_file = os.getenv('AUTH_FILE')
        self.credentials = self.create_credentials(self.credentials_file, self.scope)
        self.sheet = self.open_sheet(self.sheet_name, self.credentials)

        self.upload_frequency = 5


    def create_scope(self, scope=None):
        if scope is None:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        return scope
 
    def create_credentials(self, credentials_file=None, scope=None):
        if credentials_file is None:
            credentials_file = os.getenv('AUTH_FILE')
        return ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

    def open_sheet(self, sheet_name, credentials):
        try:
            gc = gspread.authorize(credentials)
            return gc.open(sheet_name).sheet1
        except Exception as ex:
            print(str(ex))

    def read_columns(self):
        headers = self.sheet.get('A1:AAA1')[0]
        if headers is None:
            headers = ['Id','Timestamp','Temperature','Humidity','Light','Distance']
        return headers

    def upload_data(self, data):
        if self.sheet is None:
            self.sheet = self.open_sheet(self.sheet_name, self.credentials)
        try:
            row = [data.get(column) for column in self.columns]
            self.sheet.append_row(row)
        except:
            self.sheet = None
