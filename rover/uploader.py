import sys
sys.path.append("/home/pi/rover-pi")

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import statistics
from datetime import datetime
from config.uploader_enums import Sheets_Enums
import glob


class Uploader:
    def __init__(self):

        super(Uploader, self).__init__()

        # user can pass values to these, or accept defaults as specified in Enums
        self.sheet_name = self.find_spreadsheet_name()
        self.scope = self.find_scope()
        self.credentials_file = self.find_file(
            default=Sheets_Enums.AUTH_FILE.value,
            filename="credentials.json")
        # Create sheet object, and read columns if available
        self.credentials = self.create_credentials()
        self.sheet = self.open_sheet()
        self.columns = self.read_columns()

        # data functions
        self.calculation_functions = [
            self.calculate_average,
            self.calculate_median
        ]

        # default values
        self.upload_frequency = 5
        self.null_values = Sheets_Enums.NULL_VALUES.value
        self.non_data_columns = Sheets_Enums.NON_DATA_COLUMNS.value
        self.numeric_columns = [column for column in self.columns if column not in self.non_data_columns]

    @staticmethod
    def find_file(default, filename=None):
        if filename is None:
            filename = default
        else:
            files = glob.glob(f"/home/pi/rover-pi/**/{filename}")
            if files is None:
                files = default
            elif len(files) > 1:
                print("Found more than one credentials file, using the first.")
        return files[0]

    @staticmethod
    def find_spreadsheet_name(spreadsheet_name=None):
        if spreadsheet_name is None:
            spreadsheet_name = Sheets_Enums.SPREADSHEET_NAME.value
        return spreadsheet_name

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
            return gc.open(self.sheet_name).sheet1
        except Exception as ex:
            print(str(ex))
            return None

    def read_columns(self):
        "Try to get columns from reading the sheet - if this returns None, use default values"
        headers = self.sheet.get("A1:AAA1")[0]
        if headers is None:
            headers = Sheets_Enums.DEFAULT_COLUMNS.value
            self.sheet.append_row(headers)
        return headers

    @staticmethod
    def calculate_average(array):
        """average"""
        return statistics.mean(array)

    @staticmethod
    def calculate_median(array):
        """median"""
        return statistics.median(array)


    def sheet_wrapper(function):
        "Setup necessary for Google Sheets"
        def wrapper(self,*args):
            if self.sheet is None:
                self.sheet = self.open_sheet()
            try:
                function(self, *args)
            except Exception as e:
                print(str(e))
                self.sheet = None

        return wrapper

    @sheet_wrapper
    def upload_data(self, data):
        row = [data.get(column) for column in self.columns]
        self.sheet.append_row(row)

    @sheet_wrapper
    def download_data(self):
        data = self.sheet.get_all_records()
        print('data', data)
        aggs = {
            "reading_timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        }
        print('aggs', aggs)
        for function in self.calculation_functions:
            f_name = function.__doc__
            print('name', f_name)
            aggs[f_name] = {}
            for column in self.numeric_columns:
                array = [float(row.get(column)) for row in data if row.get(column) not in self.null_values]
                aggs[f_name][column] = function(array)
        print(aggs)
        return aggs




