import sys
sys.path.append("/home/pi/rover-pi")

from flask import Flask, render_template
from datetime import datetime

from rover.uploader import Uploader

class Server(Uploader):
    def __init__(self):
        super(Server, self).__init__()
        self.app = Flask(__name__)

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
