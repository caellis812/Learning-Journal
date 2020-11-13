from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Length, EqualTo)


from models import User


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")
            ),
            name_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo('password2', message="Passwords must match.")
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired()
        ]
    )


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time_spent = TextAreaField('Time Spent', validators=[DataRequired()])
    learned = TextAreaField("What I Learned", validators=[DataRequired()])
    resources = TextAreaField("Resources To Remember", validators=[DataRequired()])
    tag1 = StringField("Entry Tags (Optional, Max of 5)")
    tag2 = StringField("Entry Tags (Optional, Max of 5)")
    tag3 = StringField("Entry Tags (Optional, Max of 5)")
    tag4 = StringField("Entry Tags (Optional, Max of 5)")
    tag5 = StringField("Entry Tags (Optional, Max of 5)")
