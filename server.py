from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

from flask import render_template

@app.route('/watch/')
@app.route('/watch/<name>')
def watch(name=None):
    return render_template('watch.html', name=name)
