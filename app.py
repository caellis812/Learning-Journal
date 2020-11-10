from flask import (Flask, g, render_template, flash, redirect, url_for)

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
    entries = models.Entry.select().order_by(models.Entry.date.desc(), models.Entry.timestamp.desc())
    return render_template('index.html', entries=entries)


@app.route('/entries/new', methods=('GET', 'POST'))
def entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        print(form.date.data)
        models.Entry.create(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            learned=form.learned.data,
            resources=form.resources.data)
        flash("Entry posted!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entries/<id>')
def detail(id):
    entry = models.Entry.get(models.Entry.id == id)
    return render_template('detail.html', entry=entry)


@app.route('/entries/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    entry = models.Entry.get(models.Entry.id == id)
    form = forms.EntryForm()
    if form.validate_on_submit():
        entry.title = form.title.data
        entry.date = form.date.data
        entry.time_spent = form.time_spent.data
        entry.learned = form.learned.data
        entry.resources = form.resources.data
        entry.save()
        flash("Entry edited!", "success")
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entry, form=form, id=id)


@app.route('/entries/<id>/deletecheck')
def deletecheck(id):
    entry = models.Entry.get(models.Entry.id == id)
    return render_template('delete.html', entry=entry)


@app.route('/entries/<id>/delete')
def delete(id):
    entry = models.Entry.get(models.Entry.id == id)
    entry.delete_instance()
    flash("Entry deleted.", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
