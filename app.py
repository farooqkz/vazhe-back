from flask import Flask, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_admin import Admin
import peewee as pw
import os
import json

from models import Word, Usage
from db import db

app = Flask(__name__)
app.secret_key = os.urandom(10)

limiter = Limiter(
    app, key_func=get_remote_address, default_limits=["1/second"]
)

admin = Admin(app)

cache = Cache()
cache.init_app(app)


@app.before_request
def db_connect():
    db.connect()


@app.teardown_request
def db_disconnect():
    if not db.is_closed():
        db.close()


def word_to_dict(word: Word) -> dict:
    w = dict()
    for attr in (
        "id",
        "word",
        "word_fa",
        "pron_eng",
        "pron_per",
        "origin",
        "badword",
    ):
        w[attr] = getattr(word, attr)
    w["usages"] = list()
    usages = Usage.select(Usage.usage).where(Usage.word == word)
    for usage in usages:
        w["usages"].append(usage.usage)

    return w


@app.route("/words", methods=("POST",))
@limiter.limit("1/second")
def create_word():
    if not request.is_json:
        abort(400)

    word = request.json.get("word")
    word_fa = request.json.get("word_fa")
    if word is None or word_fa is None:
        abort(404)

    pron_eng = request.json.get("pron_eng", "")
    pron_per = request.json.get("pron_per", "")
    origin = request.json.get("origin", "")
    badword = request.json.get("badword", False)
    usages = request.json.get("usages", [])

    word = Word.create(
        word=word,
        word_fa=word_fa,
        pron_eng=pron_eng,
        pron_per=pron_per,
        origin=origin,
        badword=badword
    )

    if len(usages) > 0:
        Usage.bulk_create(Usage(word=word, usage=u) for u in usages)
    return "well done"


@app.route("/words/<int:id_>", methods=("PUT",))
@limiter.limit("1/second")
def modify_word(id_: int):
    if not request.is_json:
        abort(400)

    word = None
    try:
        word = Word.get_by_id(id_)
    except pw.DoesNotExist:
        abort(404)

    update_dict = dict()
    for key in ("word_fa", "pron_eng", "pron_per", "origin", "badword"):
        if key in request.json:
            update_dict[key] = request.json[key]

    word.update(update_dict).execute()
    if "usages" not in request.json:
        return "well done"
    usages = request.json["usages"]
    if isinstance(usages, list):
        Usage.bulk_create(Usage(usage=u, word=word) for u in usages)

    return "well done"


@app.route("/words/<int:page>/<int:rows_num>")
@cache.memoize(timeout=3)
def words(page: int, rows_num: int):
    if page < 0 or rows_num < 10:
        abort(404)

    words = Word.select().order_by(Word.word).paginate(page, rows_num)
    words_list = list(map(word_to_dict, words))

    return {"words": words_list}


@app.route("/words/json")
@cache.cached(timeout=300)
def all_words_json():
    return {
        "words": list(map(word_to_dict, Word.select().order_by(Word.word)))
    }


@app.route("/words/pdf")
@cache.cached(timeout=900)
def all_words_pdf():
    return "Not implemented yet"
