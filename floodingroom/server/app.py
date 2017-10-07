import pkg_resources

import flask
import socketio


sio = socketio.Server()

app = flask.Flask(__name__)
app.static_folder = pkg_resources.resource_filename("floodingroom", "server/resources")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)


@sio.on('chat message', namespace='/chat')
def message(sid, data):
    print("message ", data)
    sio.emit('reply', room=sid)


@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)
