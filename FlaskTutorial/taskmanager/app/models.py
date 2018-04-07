from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

user_boards = db.Table('user_boards',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('user.id')),
                       db.Column('board_id', db.Integer, db.ForeignKey('board.id')))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), index=True,
                         unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(150), index=True, unique=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lists = db.relationship('List', backref='board', lazy='dynamic')
    users = db.relationship('User', secondary=user_boards, backref='boards')


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey(
        'board.id'))  # foreign key from board
    cards = db.relationship('Card', backref='list', lazy='dynamic')


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.String(1600), nullable=False)
    timestart = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey(
        'list.id'))  # foreign key from list
