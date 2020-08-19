from flask import Flask
from flask import render_template
import cv2, os, json

app = Flask(__name__)

with open('db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

@app.route('/')
def home():
    for name, video in db.items():
        if not os.path.isfile('./static/' + video['thumnail']):
            cap = cv2.VideoCapture('./static/' + video['path'])
            ret, img = cap.read()
            cv2.imwrite(os.path.join(os.getcwd(), 'static', 'thumnails', '%s.jpg' % name), img)
            cap.release()

    return render_template('index.html', db=db)

@app.route('/watch/')
@app.route('/watch/<name>')
def watch(name=None):
    video = db[name]
    db[name]['views'] += 1

    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f)

    return render_template('watch.html', video=video)
