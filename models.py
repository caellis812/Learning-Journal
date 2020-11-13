import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journal.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User already exists.")


class Entry(Model):
    id = AutoField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    title = TextField()
    date = DateField()
    time_spent = TextField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE


class Tag(Model):
    id = AutoField()
    content = TextField(unique=True)

    class Meta:
        database = DATABASE

    @classmethod
    def create_tag(cls, content):
        try:
            with DATABASE.transaction():
                cls.create(
                    content=content)
        except IntegrityError:
            pass


class EntryTag(Model):
    entryid = ForeignKeyField(Entry)
    tagid = ForeignKeyField(Tag)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry, Tag, EntryTag], safe=True)
    DATABASE.close()
