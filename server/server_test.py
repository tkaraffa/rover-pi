import sys
sys.path.append("/home/pi/rover-pi")
from rover.uploader import Uploader
from config.uploader_enums import Flask_Enums
from flask import Flask, render_template
from datetime import datetime

if __name__ == "__main__":
    uploader = Uploader()

    def download_data(Uploader):
        data = Uploader.sheet.get_all_records()
        aggs = {
            "reading_timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        }
        for function in Uploader.calculation_functions:
            f_name = function.__doc__
            aggs[f_name] = {}
            for column in Uploader.numeric_columns:
                array = [float(row.get(column)) for row in data if row.get(column) not in Uploader.null_values]
                aggs[f_name][column] = function(array)
        return aggs


    data = download_data(uploader)
    print(data)
    app = Flask(__name__)
    debug = True
    host = Flask_Enums.HOST.value

    @app.route('/')
    def index():
        now = datetime.now().strftime("%Y%m%dT%H%M%S")
        templateData = {
            'title': 'HELLO!',
            'time': now,
        }
        return render_template('index.html', **templateData)
    
    @app.route('/test')
    def test():
        return render_template('test.html')

    @app.route('/hello/<name>')
    def hello(name):
        return render_template('page.html', name=name)

    @app.route('/data')
    def data():
        templateData = {
            'data': str(data),
        }
        return render_template('data.html', **templateData)

    app.run(debug=debug, host=host)