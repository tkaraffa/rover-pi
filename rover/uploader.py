import sys

sys.path.append("/home/pi/rover-pi")

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import statistics
from datetime import datetime
from config.uploader_enums import Sheets_Enums
import glob
from pathlib import Path


class Uploader:
    def __init__(self):

        super(Uploader, self).__init__()

        # user can pass values to these, or accept defaults as specified in Enums
        self.sheet_name = self.find_spreadsheet_name()
        self.scope = self.find_scope()
        self.credentials_file = self.find_file(
            default=Sheets_Enums.AUTH_FILE.value, filename="credentials.json"
        )
        # Create sheet object, and read columns if available
        self.credentials = self.create_credentials()
        self.sheet = self.open_sheet()
        self.columns = self.read_columns()

        # data functions
        self.calculation_functions = {
            "average": self.calculate_average,
            "median": self.calculate_median,
            "mode": self.calculate_mode,
            "standard_deviation": self.calculate_stdev,
        }

        # default values
        self.upload_frequency = 5
        self.null_values = Sheets_Enums.NULL_VALUES.value
        self.non_data_columns = Sheets_Enums.NON_DATA_COLUMNS.value
        self.numeric_columns = [
            column
            for column in self.columns
            if column not in self.non_data_columns
        ]

    @staticmethod
    def find_file(default, filename=None):
        if filename is None:
            filename = default
        else:
            lookup = f"{Path.home()}/rover-pi/config/{filename}"
            files = glob.glob(lookup, recursive=True)
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

    @staticmethod
    def calculate_mode(array):
        """mode"""
        return statistics.mode(array)

    @staticmethod
    def calculate_stdev(array):
        """standard_deviation"""
        return statistics.stdev(array)

    def check_sheet(self):
        if self.sheet is None:
            self.sheet = self.open_sheet()

    def upload_data(self, data):
        self.check_sheet()
        try:
            row = [data.get(column) for column in self.columns]
            self.sheet.append_row(row)
        except Exception as e:
            print(str(e))
            self.sheet = None

    def download_data(self, aggregations=None):
        self.check_sheet()
        try:
            data = self.sheet.get_all_records()
            aggregated_data = {}

            if aggregations is None:
                aggregation_functions = self.calculation_functions
            else:
                aggregation_functions = {
                    func.lower(): self.calculation_functions[func.lower()]
                    for func in aggregations
                    if func
                }
            for f_name, function in aggregation_functions.items():
                aggregated_data[f_name] = {}
                for column in self.numeric_columns:
                    array = [
                        float(row.get(column))
                        for row in data
                        if row.get(column) not in self.null_values
                    ]
                    aggregated_data[f_name][column] = function(array)
            return aggregated_data
        except Exception as e:
            print(str(e))
            self.sheet = None

    def download_id_column_values(self, id_column="ID"):
        self.check_sheet()
        try:
            cell = self.sheet.find(id_column)
            column_number = cell.col
            return self.sheet.col_values(column_number)[1:]
        except Exception as e:
            print(str(e))
            self.sheet = None
            return []

    def download_most_recent_record(self):
        self.check_sheet()
        try:
            return self.sheet.get_all_records()[-1]
        except Exception as e:
            print(str(e))
            self.sheet = None