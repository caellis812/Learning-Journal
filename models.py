import datetime

from peewee import *

DATABASE = SqliteDatabase('journal.db')


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


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
