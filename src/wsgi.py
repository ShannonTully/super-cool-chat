from . import app
from . import socketio

if __name__ == "__main__":
    socketio.run(app, PORT=8000)