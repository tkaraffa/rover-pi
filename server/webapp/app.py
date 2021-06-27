from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    now = datetime.now().strftime("%Y%m%dT%H%M%S")
    templateData = {
	'title': 'Hello!',
	'time': now
    }
    return render_template('index.html', **templateData)

@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/hello/<name>')
def hello(name):
	return render_template('page.html', name=name)

if __name__=="__main__":
	app.run(debug=True, host='0.0.0.0')
