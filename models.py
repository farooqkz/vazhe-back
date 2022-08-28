import peewee as pw

from db import db

class Word(pw.Model):
    database = db

    word = pw.CharField(index=True, max_length=48)
    word_fa = pw.CharField(index=True, max_length=48)
    pron_eng = pw.TextField()
    origin = pw.CharField(index=True, max_length=48)


class Usage(pw.Model):
    database = db
    word = pw.ForeignKeyField(Word, backref="usages")
    usage = pw.TextField()


with db:
    db.create_tables([Word, Usage])
