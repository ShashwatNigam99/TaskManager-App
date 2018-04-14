from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, NewBoardForm, NewListForm, NewCardForm, SearchUsers, EditCardForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Board, List, Card
from werkzeug.urls import url_parse
from datetime import datetime
import sqlite3
# if you import forms in init then no need to write app.forms check this out


@app.route('/')
@app.route('/index/')
@login_required
def index():
    form = SearchUsers()
    return render_template('index.html', title='Home Page', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        # url parse function is used to check if a domain name is set in the
        # next variable in the url query
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>/')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

# this function executes before any view function in the application


@app.route('/showboard/<boardname>/')
@login_required
def showboard(boardname):
    board = Board.query.filter_by(name=boardname).first_or_404()
    return render_template('showboard.html', board=board)


@app.route('/showlist/<boardname>/<listname>/')
@login_required
def showlist(boardname, listname):
    listx = List.query.filter_by(title=listname).first_or_404()
    board = Board.query.filter_by(name=boardname).first_or_404()
    return render_template('showlist.html', board=board, list=listx)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/searchuser/<boardname>', methods=['GET', 'POST'])
@login_required
def searchuser(boardname):
    conn = sqlite3.connect('app.db')
    print("Database opened successfully")
    form = SearchUsers()
    print("form created")
    if form.validate_on_submit():
        srch = "'"
        srch = srch+form.usersrch.data
        print(srch)
        cur = conn.cursor()
        sql_command = 'select * from user where username like ' + srch + '%'
        sql_command += "'"
        cur.execute(sql_command)
        users = cur.fetchall()
        print(users)
        for x in users:
            print x[1]
        return redirect(url_for('showboard', boardname=boardname))
    return render_template('searchuser.html', title='Search By Username', form=form)


@app.route('/newboard/', methods=['GET', 'POST'])
@login_required
def newboard():
    form = NewBoardForm()
    if form.validate_on_submit():
        board = Board(name=form.name.data)
        current_user.boards.append(board)
        # i think the next line is redundant cuz if we check the helper table
        # double entries are made for every user table relation pair
        # board.users.append(current_user)
        db.session.add(board)
        db.session.commit()
        flash('New board created!')
        return redirect(url_for('index'))
    return render_template('newboard.html', title='Create new board', form=form)


@app.route('/newlist/<boardname>/', methods=['GET', 'POST'])
@login_required
def newlist(boardname):
    form = NewListForm()
    if form.validate_on_submit():
        board = Board.query.filter_by(name=boardname).first_or_404()
        listx = List(title=form.title.data, board_id=board.id)
        board.lists.append(listx)
        db.session.add(listx)
        db.session.commit()
        flash('New list created!')
        return redirect(url_for('showboard', boardname=boardname))
    return render_template('newlist.html', title='Create new list', form=form)


@app.route('/newcard/<boardname>/<listname>/', methods=['GET', 'POST'])
@login_required
def newcard(boardname, listname):
    form = NewCardForm()
    if form.validate_on_submit():
        board = Board.query.filter_by(name=boardname).first_or_404()
        listx = List.query.filter_by(title=listname).first_or_404()
        card = Card(name=form.name.data, desc=form.desc.data,
                    timestart=form.timestart.data, deadline=form.deadline.data, list_id=listx.id, priority=form.priority.data.upper())
        listx.cards.append(card)
        db.session.add(card)
        db.session.commit()
        flash('New card created!')
        return redirect(url_for('showlist', boardname=boardname, listname=listname))
    return render_template('newcard.html', title='Create new card', form=form)


@app.route('/showcard/<boardname>/<listname>/<cardname>/')
@login_required
def showcard(boardname, listname, cardname):
    listx = List.query.filter_by(title=listname).first_or_404()
    board = Board.query.filter_by(name=boardname).first_or_404()
    card = Card.query.filter_by(name=cardname).first_or_404()
    return render_template('showcard.html', board=board, list=listx, card=card)


@app.route('/deletecard/<boardname>/<listname>/<cardname>')
@login_required
def deletecard(boardname, listname, cardname):
    listx = List.query.filter_by(title=listname).first_or_404()
    board = Board.query.filter_by(name=boardname).first_or_404()
    card = Card.query.filter_by(name=cardname).first_or_404()
    listx.cards.remove(card)
    db.session.delete(card)
    db.session.commit()
    return render_template('showlist.html', board=board, list=listx)


@app.route('/deletelist/<boardname>/<listname>')
@login_required
def deletelist(boardname, listname):
    listx = List.query.filter_by(title=listname).first_or_404()
    board = Board.query.filter_by(name=boardname).first_or_404()
    board.lists.remove(listx)
    db.session.delete(listx)
    db.session.commit()
    return render_template('showboard.html', board=board)


@app.route('/deleteboard/<boardname>')
@login_required
def deleteboard(boardname):
    board = Board.query.filter_by(name=boardname).first_or_404()
    current_user.boards.remove(board)
    db.session.delete(board)
    db.session.commit()
    return render_template('index.html')

@app.route('/editcard/<boardname>/<listname>/<cardname>', methods=['GET', 'POST'])
@login_required
def editcard(boardname, listname, cardname):
    board = Board.query.filter_by(name=boardname).first_or_404()
    listx = List.query.filter_by(title=listname).first_or_404()
    card = Card.query.filter_by(name=cardname).first_or_404()
    form=EditCardForm()
    if form.validate_on_submit():
        card.name = form.name.data
        card.desc = form.desc.data
        card.timestart = form.timestart.data
        card.deadline = form.deadline.data
        card.priority = form.priority.data.upper()
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('showcard',boardname=board.name,listname=listx.title,cardname=card.name))
    elif request.method == 'GET':
        form.name.data = card.name
        form.desc.data = card.desc
        form.timestart.data = card.timestart
        form.deadline.data = card.deadline
        form.priority.data = card.priority
    return render_template('editcard.html', title='Edit Card',
                           form=form)
