import sys

sys.path.append("/home/pi/rover-pi")

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import statistics
from config.uploader_enums import Sheets_Enums
import glob
from pathlib import Path


class Uploader:
    """Class for interacting with Google Sheets

    Attibutes
    ---------
    sheet_name: str
        The name of the Google Sheet in which to record data

    scope: list
        The Google API scope

    credentials_file: str
        The file that holds the Google Service Account credentials

    credentials
        The actual Google Service Account credentials

    sheet
        The Google Sheet to operate on

    columns: list
        The headers of the Google Sheet file

    calculation_functions: dict
        The key/value pairs of metrics and their calculation funcionts

    upload_frequency: int
        The rate at which to upload data

    null_values: list
        Values to interpret as Null

    non_data_columns: list
        Columns for which to avoid calculating metrics

    numeric_columns: list
        Columns for which to calculate metrics
    """

    def __init__(self) -> None:

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
    def find_file(default, filename: str = None) -> str:
        """Finds the file containing Google Service Account credentials

        Parameters
        ----------
        default: str
            The default filename to look for

        filename: str
            The provided filename to look for

        Returns
        -------
        file: str
            The path to the credentials file"""
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
    def find_spreadsheet_name(spreadsheet_name: str = None) -> str:
        """Finds the spreadsheet name. If not provided,
        uses a default value

        Parameters
        ----------
        spreadsheet_name: str, optional
            The name of the spreadhseet to use

        Returns
        -------
        spreadsheet_name: str
        """
        if spreadsheet_name is None:
            spreadsheet_name = Sheets_Enums.SPREADSHEET_NAME.value
        return spreadsheet_name

    @staticmethod
    def find_scope(scope: list = None) -> list:
        """Finds the Google API scope. If not provided,
        uses a default value

        Parameters
        ----------
        scope: list
            The scope to use

        Returns
        -------
        scope: list
        """
        if scope is None:
            scope = Sheets_Enums.DEFAULT_SCOPE.value
        return scope

    def create_credentials(self) -> dict:
        """Creates Service Account Credentials to use for
        authentication

        Returns
        -------
        credentials
            The credentials to pass to gspread.authorize()
        """
        return ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_file, self.scope
        )

    def open_sheet(self):
        """Opens the Sheet object to write to

        Returns
        -------
        sheet
            The opened Google Sheet object

        Raises
        ------
        Any exception if met
        """
        try:
            gc = gspread.authorize(self.credentials)
            return gc.open(self.sheet_name).sheet1
        except Exception as ex:
            print(str(ex))
            return None

    def read_columns(self) -> list:
        """Tries to get columns from reading the Sheet object.
        If none are found (i.e., the sheet is empty),
        uses default values

        Returns
        -------
        headers: list
            The headers of the Sheet object
        """
        headers = self.sheet.get("A1:AAA1")[0]
        if headers is None:
            headers = Sheets_Enums.DEFAULT_COLUMNS.value
            self.sheet.append_row(headers)
        return headers

    @staticmethod
    def calculate_average(array) -> float:
        """Calculates the average of the provided array."""
        return statistics.mean(array)

    @staticmethod
    def calculate_median(array) -> float:
        """Calculates the median of the provided array."""
        return statistics.median(array)

    @staticmethod
    def calculate_mode(array) -> float:
        """Calculates the mode of the provided array."""
        return statistics.mode(array)

    @staticmethod
    def calculate_stdev(array) -> float:
        """Calculates the standard deviation of the provided array."""
        return statistics.stdev(array)

    def check_sheet(self) -> None:
        """Ensures the Sheet object is already open
        before attempting any opeations"""
        if self.sheet is None:
            self.sheet = self.open_sheet()

    def upload_data(self, data: dict) -> None:
        """Uploads data to the class's Sheet object

        Parameters
        ----------
        data: dict
            The JSON-formatted data

        Raises
        ------
        Any exception if met, and resets the Sheet object"""
        self.check_sheet()
        try:
            row = [data.get(column) for column in self.columns]
            self.sheet.append_row(row)
        except Exception as e:
            print(str(e))
            self.sheet = None

    def download_data(self, aggregations: list = None) -> dict:
        """Downloads data from the sheet for the provided aggregations.
        If not provided, uses the default battery of aggregations
        (mean, median, mode, std dev)

        Parameters
        ----------
        aggregations: list, optional
            The aggregations to perform

        Returns
        -------
        aggregated_data: dict
            The JSON-formatted aggregated data

        Raises
        ------
            Any exception if met, and resets the Sheet object
        """
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

    def download_id_column_values(self, id_column: str = "ID") -> list:
        """Downloads the ID column

        Parameters
        ----------
        id_column: str, default="ID"
            The name of the column that contains ID values

        Returns
        -------
        ids: list
            The list of ID values

        Raises
        ------
            Any exception if met, and resets the Sheet object
        """
        self.check_sheet()
        try:
            cell = self.sheet.find(id_column)
            column_number = cell.col
            return self.sheet.col_values(column_number)[1:]
        except Exception as e:
            print(str(e))
            self.sheet = None
            return []

    def download_most_recent_record(self) -> dict:
        """Downloads the most recent record from the sheet

        Returns
        -------
        record: dict
            The JSON representation of the most recent record.

        Raises
        ------
            Any exception if met, and resets the Sheet object
        """
        self.check_sheet()
        try:
            return self.sheet.get_all_records()[-1]
        except Exception as e:
            print(str(e))
            self.sheet = None
