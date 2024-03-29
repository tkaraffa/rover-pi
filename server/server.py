from re import S
import sys

sys.path.append("/home/pi/rover-pi")

from flask import Flask, render_template
from datetime import datetime
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json
from rover.uploader import Uploader
from config.uploader_enums import Flask_Enums


class Server(Uploader):
    """Server class for hosting a Flask webpage server.

    Attributes
    ----------
    app:
        The Flask application
    debug: bool
        Debug mode
    host: str
        The Host location
    app.config:
        Configurations for the application

    """

    def __init__(self):
        super(Server, self).__init__()

        self.app = Flask(__name__)
        self.debug = True
        self.host = Flask_Enums.HOST.value

        self.app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

        @self.app.route("/")
        def index():
            now = datetime.now().strftime("%Y%m%dT%H%M%S")
            ignore_matches = Flask_Enums.IGNORED_URLS.value
            links = []
            for rule in self.app.url_map.iter_rules():
                links.append((rule.endpoint))
            print(links)
            templateData = {
                "title": "RPiRover",
                "time": now,
                "links": links,
            }
            return render_template("index.html", **templateData)

        @self.app.route("/test")
        def test():
            return render_template("test.html")

        @self.app.route("/hello/<name>")
        def hello(name):
            return render_template("page.html", name=name.title())

        @self.app.route("/data/")
        def data(aggs=None):
            templateData = self.create_data_for_pages(aggs)
            return render_template("data.html", **templateData)

        @self.app.route("/data/<aggs>")
        def data_agg(aggs=None):
            templateData = self.create_data_for_pages(aggs)
            return render_template("data.html", **templateData)

        @self.app.route("/vis/")
        def vis(columns=None):
            templateData = self.create_visualizations(columns)
            return render_template("vis.html", **templateData)

        @self.app.route("/vis/<columns>")
        def vis_col(columns=None):
            templateData = self.create_visualizations(columns)
            return render_template("vis.html", **templateData)

    @staticmethod
    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    def create_data_for_pages(self, aggs: str = None):
        """Creates aggreagates to display on webpage

        Parameters
        ----------
        aggs: str
            Aggregates read from the page's URL to display

        Returns
        -------
        tempteData: dict
            Dictionary containing data to dispaly, ready to parse in Jinja template
        """
        if aggs is not None:
            aggs = aggs.split(",")
            data = self.download_data(aggs)
        else:
            data = []
            aggs = []
        id_data = self.download_id_column_values()
        count = len(id_data)
        unique_ids = len(set(id_data))
        last_record = self.download_most_recent_record()

        templateData = {
            "title": "Data",
            "data": data,
            "count": count,
            "unique_ids": unique_ids,
            "sheet": self.sheet_name,
            "last_record": last_record,
            "buttons": self.calculation_functions,
            "aggs": aggs,
        }
        return templateData

    def create_visualizations(self, columns=None):
        """Creates visualizations to display

        Parameters
        ----------
        columns: str
            Columns read from the page's URL to display

        Returns
        -------
        templateData: dict
            Dictionary containing data to dispaly, ready to parse in Jinja template
        """
        if columns is not None:
            columns = columns.split(",")
            data = self.sheet.get_all_records(columns)
        else:
            data = []
            columns = []
        buttons = self.numeric_columns
        timestamps = [row["Timestamp"] for row in data]
        column_data = [
            [row[column.title()] for row in data] for column in columns
        ]
        graphJSONs = {
            column: json.dumps(
                go.Figure(
                    go.Scatter(
                        x=timestamps, y=data, mode="markers", name=column
                    ),
                    layout={
                        "title": column,
                        "legend_title": "Measurements",
                        "showlegend": True,
                    },
                ),
                cls=PlotlyJSONEncoder,
            )
            for column, data in zip(columns, column_data)
        }
        templateData = {
            "title": "Visualizations",
            "sheet": self.sheet_name,
            "timestamps": timestamps,
            "column_data": column_data,
            "columns": columns,
            "buttons": buttons,
            "graphJSONs": graphJSONs,
        }
        return templateData

    def run(self):
        self.app.run(debug=self.debug, host=self.host)
