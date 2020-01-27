import os
import re
import struct
import json

import redis
from yhttp import Application, text, statuses, validate
from hashids import Hashids


URL_PATTERN=re.compile(
    r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}' \
    r'\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
)


URL_TIMETOLIVE = 48 * 3600
hashids = Hashids()
app = Application()
redis = redis.Redis(host='localhost', port='6379')


def getfreshid():
    randomint, = struct.unpack('L', os.urandom(8))
    return hashids.encode(randomint)


def store(url):
    while True:
        freshid = getfreshid()
        if db.redis.setnx(freshid, url):
            break

    db.redis.expire(freshid, URL_TIMETOLIVE)
    return freshid


@app.route('/(.*)')
def get(req, key):
    originalurl = db.redis.get(key)
    if not originalurl:
        raise statuses.notfound()

    raise statuses.found(originalurl.decode())


@app.route()
@validate(fields=dict(
    url=dict(required='400 Field missing: url')
))
@text
def post(req):
    longurl = req.form['url']
    if not URL_PATTERN.match(longurl):
        raise statuses.badrequest()

    shorturl = store(longurl)
    req.response.status = '201 Created'
    return shorturl

