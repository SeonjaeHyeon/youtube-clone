# youtube-clone
Build a YouTube Clone with Python 3 and Flask  

Still working in progress.. Images will be added when cloning is completed.  

## How to Run
First, you need to use the flask command or python's `-m` switch with Flask.
```
$ export FLASK_APP=server.py
$ flask run
 * Running on http://127.0.0.1:5000/
```

Windows
```
>set FLASK_APP=server.py
>flask run
 * Running on http://127.0.0.1:5000/
```

**Alternative way**
```
$ export FLASK_APP=server.py
$ python -m flask run
 * Running on http://127.0.0.1:5000/
```

Then, a development server which is enough to test yourself will be started.  
Now you can see the result if you connect to `http://127.0.0.1:5000/` with any web browser.

## Requirements
- [Flask v1.1+](https://flask.palletsprojects.com/en/1.1.x/)  
- [opencv-python v.4.4+](https://pypi.org/project/opencv-python/)  

Following dependencies will be installed automatically when installing Flask.
- Jinja2 v2.11+  
- Werkzeug v1.0+  
- MarkupSafe v1.1+  
- ItsDangerous v1.1+  
- Click v7.1+  
