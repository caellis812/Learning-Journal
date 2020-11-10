from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from flask_bcrypt import check_password_hash

import models
import forms

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'aslkdfjoiewnoifboivj9832u'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        flash("Welcome. You've been registered.", "success")
        models.User.create_user(
            username=form.username.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Your username or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You're logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your username or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You're logged out! See you soon.", "success")
    return redirect(url_for('index'))


@app.route('/')
@app.route('/entries')
def index():
    entries = models.Entry.select().order_by(models.Entry.date.desc(), models.Entry.timestamp.desc())
    return render_template('index.html', entries=entries)


@app.route('/entries/new', methods=('GET', 'POST'))
@login_required
def entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
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
@login_required
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
@login_required
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
    try:
        models.User.create_user(
            username='testuser',
            password='testpassword'
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
