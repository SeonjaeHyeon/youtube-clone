from flask import Flask
import cv2, os

app = Flask(__name__)

@app.route('/')
def home():
    file_list = os.listdir('./static/videos/')
    video_list = [file for file in file_list if file.endswith(".mp4")] # https://itholic.github.io/python-listdir-glob/

    for f in video_list:
        if not os.path.isfile('./static/thumbnails/' + f[:-4] + '.jpg'):
            cap = cv2.VideoCapture('./static/videos/' + f)
            ret, img = cap.read()
            # why use os.getcwd(): https://daeunginfo.blogspot.com/2019/07/opencv-python-error-215assertion-failed.html?m=1
            cv2.imwrite(os.path.join(os.getcwd(), 'static', 'thumnails', '%s.jpg' % f[:-4]), img)
            cap.release()

    return render_template('index.html')

from flask import render_template

@app.route('/watch/')
@app.route('/watch/<name>')
def watch(name=None):
    return render_template('watch.html', name=name)
