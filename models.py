import peewee as pw

from db import db


class BaseModel(pw.Model):
    class Meta:
        database = db


class Word(BaseModel):
    word = pw.CharField(index=True, max_length=48)
    word_fa = pw.CharField(index=True, max_length=48)
    badword = pw.BooleanField()
    pron_eng = pw.TextField()
    pron_per = pw.TextField()
    origin = pw.CharField(index=True, max_length=48)


class Usage(BaseModel):
    word = pw.ForeignKeyField(Word, backref="usages")
    usage = pw.TextField()


with db:
    db.create_tables([Word, Usage])
