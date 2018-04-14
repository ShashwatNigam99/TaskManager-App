from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')


class NewBoardForm(FlaskForm):
    name = StringField('Board Name:', validators=[DataRequired()])
    submit = SubmitField('Create New Board')


class NewListForm(FlaskForm):
    title = StringField('List title', validators=[DataRequired()])
    submit = SubmitField('Create New List')


class NewCardForm(FlaskForm):
    name = StringField('Card name', validators=[DataRequired()])
    desc = TextAreaField('Description', validators=[
                         Length(min=30, max=1600), DataRequired()])
    timestart = DateField('Start')
    deadline = DateField('Deadline', validators=[DataRequired()])
    priority = StringField('Priority', validators=[DataRequired()])
    submit = SubmitField('Create New Card')

    def validate_priority(self,priority):
        if priority.data.lower() != 'low' and priority.data.lower() != 'medium' and priority.data.lower() != 'high':
            raise ValidationError('Invalid Priority')


class SearchUsers(FlaskForm):
    usersrch = StringField('Search by username', validators=[DataRequired()])
    submit = SubmitField('Search users')


class EditCardForm(FlaskForm):
    name = StringField('Card name', validators=[DataRequired()])
    desc = TextAreaField('Description', validators=[
                         Length(min=30, max=1600), DataRequired()])
    timestart = DateField('Start')
    deadline = DateField('Deadline', validators=[DataRequired()])
    priority = StringField('Priority', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

    def validate_priority(self,priority):
        if priority.data.lower() != 'low' and priority.data.lower() != 'medium' and priority.data.lower() != 'high':
            raise ValidationError('Invalid Priority')
