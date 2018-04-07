from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False))
    password_hash=db.Column(db.String(128), nullable = False))
    email=db.Column(db.String(150), index=True, unique=True, nullable=False))

class Board(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    lists=db.relationship('List', backref='board', lazy='dynamic')
    # users = db.relationship('User', secondary=user_boards, backref='boards')

class List(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(30))
    board_id=db.Column(db.Integer, db.ForeignKey(
        'board.id'))  # foreign key from board
    cards=db.relationship('Card', backref='list', lazy='dynamic')

class Card(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64), nullable=False)
    desc=db.Column(db.String(1600), nullable=False)
    timestart=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deadline=db.Column(db.DateTime, nullable=False)
    list_id=db.Column(db.Integer, db.ForeignKey(
        'list.id'))  # foreign key from list
