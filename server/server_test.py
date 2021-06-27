import sys
sys.path.append("/home/pi/rover-pi")
from rover.uploader import Uploader
from config.uploader_enums import Flask_Enums
from flask import Flask, render_template
from datetime import datetime

if __name__ == "__main__":
    uploader = Uploader()
    data = uploader.download_data()
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