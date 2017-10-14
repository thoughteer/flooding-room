from floodingroom.server.app import app
from floodingroom.server.sio import sio


if __name__ == "__main__":
    sio.run(app, host="192.168.1.173", port=8080)
