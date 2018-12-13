from flask import Flask
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


from . import routes, models
