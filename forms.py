from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField
from wtforms.validators import (DataRequired)


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time_spent = TextAreaField('Time Spent', validators=[DataRequired()])
    learned = TextAreaField("What I Learned", validators=[DataRequired()])
    resources = TextAreaField("Resources To Remember", validators=[DataRequired()])
