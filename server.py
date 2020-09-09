from flask import Flask, render_template, request
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
    with open('db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    video = db[name]
    db[name]['views'] += 1

    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=4)

    time = int(request.args.get('t', 0))

    return render_template('watch.html', video=video, time=time)

@app.route('/rate')
def rate():
    try:
        if request.method != 'GET':
            return 'Wrong request method.'

        with open('db.json', 'r', encoding='utf-8') as f:
            db = json.load(f)

        param = request.args.to_dict()

        if param['type'] == 'like':
            if param['mode'] == 'submit':
                db[param['name']]['rate']['like'] += 1
            elif param['mode'] == 'cancel':
                db[param['name']]['rate']['like'] -= 1
            elif param['mode'] == 'change':
                db[param['name']]['rate']['like'] += 1
                db[param['name']]['rate']['dislike'] -= 1
        elif param['type'] == 'dislike':
            if param['mode'] == 'submit':
                db[param['name']]['rate']['dislike'] += 1
            elif param['mode'] == 'cancel':
                db[param['name']]['rate']['dislike'] -= 1
            elif param['mode'] == 'change':
                db[param['name']]['rate']['dislike'] += 1
                db[param['name']]['rate']['like'] -= 1

        with open('db.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=4)
    except:
        return json.dumps({'message':'failed'})
    
    return json.dumps({'message':'success'})
