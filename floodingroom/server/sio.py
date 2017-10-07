import flask
import flask_socketio

from .app import app


class SIO(flask_socketio.SocketIO):

    def __init__(self):
        flask_socketio.SocketIO.__init__(self, app)
        self.__configure()

    def __configure(self):

        @self.on("connect")
        def connect():
            print("connect ", flask.request.sid)

        @self.on("ready")
        def accept(json):
            self.emit("accept")

        @self.on("disconnect")
        def disconnect():
            print("disconnect ", flask.request.sid)


sio = SIO()
