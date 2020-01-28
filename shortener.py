import os
import struct

import redis
from hashids import Hashids
from yhttp import Application, text, statuses, validate


hashids = Hashids()
app = Application()
redis = redis.Redis(host='localhost', port='6379')


def store(url):
    randomint, = struct.unpack('L', os.urandom(8))
    freshid = hashids.encode(randomint)
    redis.set(freshid, url)
    return freshid


@app.route('/(.*)')
def get(req, key):
    originalurl = redis.get(key)
    if not originalurl:
        raise statuses.notfound()

    raise statuses.found(originalurl.decode())


@app.route()
@validate(fields=dict(
    url=dict(
        required='400 Field missing: url',
        pattern=(r'^http://.*', '400 Invalid URL')
    )
))
@text
def post(req):
    longurl = req.form['url']
    shorturl = store(longurl)
    req.response.status = '201 Created'
    return shorturl

