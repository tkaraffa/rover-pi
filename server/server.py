import sys
sys.path.append("/home/pi/rover-pi")

from flask import Flask, render_template
from datetime import datetime
import json

from rover.uploader import Uploader
from config.uploader_enums import Flask_Enums

class Server(Uploader):
    def __init__(self):
        super(Server, self).__init__()

        self.app = Flask(__name__)
        self.debug = True
        self.host = Flask_Enums.HOST.value

        self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


        @self.app.route('/')
        def index():
            now = datetime.now().strftime("%Y%m%dT%H%M%S")
            templateData = {
                'title': 'HELLO!',
                'time': now,
            }
            return render_template('index.html', **templateData)
        
        @self.app.route('/test')
        def test():
            return render_template('test.html')

        @self.app.route('/hello/<name>')
        def hello(name):
            return render_template('page.html', name=name)

        @self.app.route('/data/<aggs>')
        def data(aggs):
            aggs = aggs.split(",")
            data = self.download_data(aggs)
            id_data = self.download_id_column_values()
            count = len(id_data)
            unique_ids = len(set(id_data)),
            last_record = self.download_most_recent_record()

            templateData = {
                'data': data,
                'count': count,
                'unique_ids': unique_ids,
                'sheet': self.sheet_name,
                'last_record': last_record,
            }
            return render_template('data.html', **templateData)

    def run(self):
        self.app.run(debug=self.debug, host=self.host)

    