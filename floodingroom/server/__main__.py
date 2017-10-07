import pkg_resources

import socketio
import eventlet
import eventlet.wsgi
import flask
from flask import Flask, render_template

sio = socketio.Server()
app = Flask(__name__)
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


if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    middleware = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8080)), middleware)
