from flask import (Flask, g, render_template, flash, redirect, url_for)
import datetime

import models
import forms

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'aslkdfjoiewnoifboivj9832u'


@app.before_request
def before_request():
    """Connect to the database"""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response


@app.route('/')
@app.route('/entries')
def index():
    entries = models.Entry.select().limit(100)
    return render_template('index.html', entries=entries)


@app.route('/entries/new', methods=('GET', 'POST'))
def entry():
    form = forms.EntryForm()
    print(form.title.data, form.timeSpent.data, form.whatILearned.data, form.ResourcesToRemember.data)
    if form.validate_on_submit():
        models.Entry.create(
            title=form.title.data,
            #date=form.date.data,
            time_spent=form.timeSpent.data,
            learned=form.whatILearned.data,
            resources=form.ResourcesToRemember.data)
        flash("Entry posted!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
    models.Entry.create(
        title="TEST ENTRY ON RUN OF APP.PY",
        time_spent="TEST",
        learned="TEST",
        resources="TEST")
