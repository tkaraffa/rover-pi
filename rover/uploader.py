import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from rover_enums import Sheets_Enums


class Uploader:
    def __init__(self):
        super(Uploader, self).__init__()

        # user can pass values to these, or accept defaults as specified in Enums
        self.sheet_name = self.find_spreadsheet_name()
        self.scope = self.find_scope()
        self.credentials_file = self.find_credentials_file()

        # Create sheet object, and read columns if available
        self.credentials = self.create_credentials()
        self.sheet = self.open_sheet()
        self.columns = self.read_columns()

        # default values
        self.upload_frequency = 5

    @staticmethod
    def find_spreadsheet_name(spreadsheet_name=None):
        if spreadsheet_name is None:
            spreadsheet_name = Sheets_Enums.SPREADSHEET_NAME.value
        return spreadsheet_name

    @staticmethod
    def find_credentials_file(credentials_file=None):
        if credentials_file is None:
            credentials_file = os.path.join(
                os.path.dirname(__file__),
                Sheets_Enums.AUTH_FILE.value
            )
        return credentials_file

    @staticmethod
    def find_scope(scope=None):
        if scope is None:
            scope = Sheets_Enums.DEFAULT_SCOPE.value
        return scope

    def create_credentials(self):
        return ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_file, self.scope
        )

    def open_sheet(self):
        try:
            gc = gspread.authorize(self.credentials)
            print(self.sheet_name)
            return gc.open(self.sheet_name).sheet1
        except Exception as ex:
            print(str(ex))

    def read_columns(self):
        "Try to get columns from reading the sheet - if this returns None, use default values"
        headers = self.sheet.get("A1:AAA1")[0]
        if headers is None:
            headers = Sheets_Enums.DEFAULT_COLUMNS.value
            self.sheet.append_row(headers)
        return headers

    def upload_data(self, data):
        if self.sheet is None:
            self.sheet = self.open_sheet(self.sheet_name, self.credentials)
        try:
            row = [data.get(column) for column in self.columns]
            self.sheet.append_row(row)
        except:
            self.sheet = None
