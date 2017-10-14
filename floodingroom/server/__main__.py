from floodingroom.server.app import app
from floodingroom.server.sio import sio


if __name__ == "__main__":
    sio.run(app, port=8080)
