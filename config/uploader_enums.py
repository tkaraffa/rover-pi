from enum import Enum


class Directories(Enum):
    DATA_DIRECTORY = "atmosphere-sensor-data"
    OUTPUT_FILE = "atmosphere-sensor-data.json"


class SheetsEnums(Enum):
    AUTH_FILE = "credentials.json"
    SPREADSHEET_NAME = "community_env_data"
    DEFAULT_SCOPE = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    DEFAULT_COLUMNS = [
        "ID",
        "Timestamp",
        "Temperature",
        "Humidity",
        "Light",
        "Distance",
    ]
    NULL_VALUES = [
        "",
        None,
        "NA",
        "N/A",
        "na",
        "n/a",
        "\n",
        "None",
        "none",
        "NULL",
        "Null",
        "null",
        False,
    ]
    NON_DATA_COLUMNS = [
        "ID",
        "Timestamp",
    ]


class Flask_Enums(Enum):
    HOST = "0.0.0.0"
    IGNORED_URLS = ["<", ">", "test", "static"]
