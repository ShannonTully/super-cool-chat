from . import app

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.String(256), unique=True)
    username = db.Column(db.String(256), unique=True)
    # is_validated = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f'<User: {self.username}>'