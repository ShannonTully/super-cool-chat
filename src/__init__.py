# from . import models
from flask import Flask
from flask_socketio import SocketIO
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    instance_relative_config=True
)

app.config.from_mapping(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

socketio = SocketIO(app)


# @socketio.on('connect', namespace='/connect')
# def connect(sid, data):
#     return 'wut'


@socketio.on('aaa')
def test_connect():
    print("Welcome, aaa received")
    socketio.emit('aaa_response', {'data': 'Server'})


if __name__ == "__main__":
    socketio.run(app, PORT=8000)
