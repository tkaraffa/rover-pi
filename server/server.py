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
            templateData = {
                'data': json.dumps(self.download_data([aggs]), indent=2),
                'agg': aggs
            }
            return render_template('data.html', **templateData)

    def run(self):
        self.app.run(debug=self.debug, host=self.host)

    