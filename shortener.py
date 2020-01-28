import os

import redis
from hashids import Hashids
from yhttp import Application, text, statuses, validate, statuscode


hashids = Hashids()
app = Application()
redis = redis.Redis(host='localhost', port='6379')


def store(url):
    freshid = hashids.encode(int.from_bytes(os.urandom(8), 'big'))
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
@statuscode('201 Created')
def post(req):
    return store(req.form['url'])

