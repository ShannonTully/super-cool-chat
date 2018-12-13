from . import app
from .models import db, User
from .words import animals, adjectives

from sqlalchemy.exc import IntegrityError
from random import choice
from uuid import uuid4
import socketio
import json

sio = socketio.AsyncServer()


@app.route('/')
def home():
    return 'TODO: entry stuff'


@app.route('/signup/<password>/', methods=['POST'])
def login(password):
    if password == 'catsrcoolmeow':
        try:
            user_id = str(uuid4())
            username = f'{str(choice(adjectives)).title()} {str(choice(animals)).title()}'
            user = {
                'user_id': user_id,
                'username': username,
            }

            db.session.add(User(**user))
            db.session.commit()
            return f'Your access id is:\n{user_id}\nSAVE THIS AND DO NOT SHARE!\n\nYour temporary username is:\n{username}'
        except IntegrityError:
            return 'Sorry, something failed on our end. Try again.'

    return 'Wrong password'


@app.route('/list/<user_id>/')
def list_users(user_id):
    user_list = db.session.query(User).all()

    for user in user_list:
        if user_id == user.user_id:
            return json.dumps([users.username for users in user_list])

    return 'You are not an authorized user.'


@app.route('/change_username/<user_id>/<new_name>/', methods=['PUT'])
def change_username(user_id, new_name):
    user_list = db.session.query(User).all()

    for user in user_list:
        if user_id == user.user_id:
            try:
                user.username = new_name
                db.session.commit()
                return f'Your username is now {new_name}'
            except IntegrityError:
                return 'Sorry that username is taken.'

    return 'You are not an authorized user.'


@sio.on('connect', namespace='/connect')
def connect(sid, data):
    return 'wut'
