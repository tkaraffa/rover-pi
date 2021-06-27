import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import statistics
import json
from datetime import datetime
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
    def find_spreadsheet_name(spreadsheet_name=None):
        if spreadsheet_name is None:
            spreadsheet_name = Sheets_Enums.SPREADSHEET_NAME.value
        return spreadsheet_name

    @staticmethod
    def find_credentials_file(credentials_file=None):

        if credentials_file is None:
            credentials_file = os.path.join(
                os.path.dirname(__file__), Sheets_Enums.AUTH_FILE.value
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
        def wrapper(self,**kwargs):
            if self.sheet is None:
                self.sheet = self.open_sheet()
            try:
                function(self, **kwargs)
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
        aggs = {
            "reading_timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        }
        for function in self.calculation_functions:
            f_name = function.__doc__
            aggs[f_name] = {}
            for column in self.numeric_columns:
                array = [float(row.get(column)) for row in data if row.get(column) not in self.null_values]
                aggs[f_name][column] = function(array)
        print(json.dumps(aggs, indent=2))
        return aggs




