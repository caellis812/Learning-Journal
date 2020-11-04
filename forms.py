from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField
from wtforms.validators import (DataRequired)

class EntryForm(FlaskForm):
    title = StringField('Title')
    # date = DateField('Date')
    timeSpent = TextAreaField('Time Spent')
    whatILearned = TextAreaField("What I Learned")
    ResourcesToRemember = TextAreaField("Resources To Remember")