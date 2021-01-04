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

    db_list = [{"name": k, "data": v} for k, v in db.items()]
    for i, j in enumerate(db_list):
        if j.get("name") == name:
            if i + 1 == len(db_list):
                next_video = db_list[0]
            else:
                next_video = db_list[i + 1]

    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=4)

    time = int(request.args.get('t', 0))

    return render_template('watch.html', video=video, time=time, next_video=next_video)

@app.route('/results', methods=['POST'])
def results():
    try:
        if request.method != 'POST':
            return 'Wrong request method.'

        with open('db.json', 'r', encoding='utf-8') as f:
            db = json.load(f)

        params = request.json
        keyword = params.get('keyword')

        if keyword is not None and keyword != '':
            result = {}

            for key, value in db.items():
                title = value.get('title')

                if keyword in title:
                    result[key] = title

        if result == {}:
            return json.dumps({'message': 'success', 'has_result': False})
    except:
        return json.dumps({'message': 'failed'})

    return json.dumps({'message': 'success', 'has_result': True, 'result': result})

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

@app.route('/view')
def view():
    try:
        if request.method != 'GET':
            return 'Wrong request method.'

        with open('db.json', 'r', encoding='utf-8') as f:
            db = json.load(f)

        param = request.args.to_dict()
        db[param['name']]['views'] += 1

        with open('db.json', 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=4)
    except:
        return json.dumps({'message':'failed'})

    return json.dumps({'message':'success'})
