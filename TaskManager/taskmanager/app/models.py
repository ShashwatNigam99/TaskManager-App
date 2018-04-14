from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

user_boards = db.Table('user_boards',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('user.id')),
                       db.Column('board_id', db.Integer, db.ForeignKey('board.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), index=True,
                         unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(150), index=True, unique=True, nullable=False)
    about_me = db.Column(db.String(150))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lists = db.relationship('List', backref='board', cascade="all,delete", lazy='dynamic')
    users = db.relationship('User', secondary=user_boards, cascade="all,delete", backref='boards')


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey(
        'board.id'))  # foreign key from board
    cards = db.relationship('Card', backref='list', cascade="all,delete", lazy='dynamic')


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.String(1600), nullable=False)
    timestart = db.Column(db.Date, index=True, nullable=False, default=datetime.date(datetime.utcnow()))
    deadline = db.Column(db.Date, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey(
        'list.id'))  # foreign key from list
    priority = db.Column(db.String(5), nullable=False)    



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
