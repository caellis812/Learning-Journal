import datetime

from peewee import *

DATABASE = SqliteDatabase('journal.db')


class Entry(Model):
    id = AutoField()
    title = TextField()
    #date = DateField()
    time_spent = TextField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-date',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
