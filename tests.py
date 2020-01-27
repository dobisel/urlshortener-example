import os
import string

import pytest
from bddrest import Given, status, when, response, given

from shortener import app


@pytest.fixture
def urandommock():
    backup = os.urandom
    os.urandom = lambda c: string.ascii_letters.encode()[:c]
    yield
    os.unrandom = backup


@pytest.fixture
def redismock():
    import shortener

    class RedisMock:
        maindict: dict

        def __init__(self):
            self.maindict = dict()

        def get(self, key: str):
            return self.maindict.get(key, '').encode()

        def set(self, key: str, value):
            self.maindict[key] = value

        def setnx(self, key: str, value):
            if not self.maindict.get(key):
                self.set(key, value)
                return 1
            return 0

        def expire(self, key: str, seconds: int):
            pass

    dummy = RedisMock()
    backup = shortener.redis
    shortener.redis = dummy
    yield dummy
    shortener.redis = backup


def test_shortener_json(urandommock, redismock):
    with Given(
        app,
        title='Shortening a URL',
        verb='POST',
        json=dict(url='http://example.com')
    ):
        assert status == 201
        assert response.text == 'rmXGPMVQnrKAB'

        when(title='URL is not valid', json=dict(url='invalidurl'))
        assert status == 400

        when(title='URL field is missing', json=given - 'url')
        assert status == '400 Field missing: url'


def test_shortener_urlencoded(urandommock, redismock):
    with Given(
        app,
        title='Shortening a URL',
        verb='POST',
        form=dict(url='http://example.com')
    ):
        assert status == 201
        assert response.text == 'rmXGPMVQnrKAB'


def test_shortener_multipart(urandommock, redismock):
    with Given(
        app,
        title='Shortening a URL',
        verb='POST',
        multipart=dict(url='http://example.com')
    ):
        assert status == 201
        assert response.text == 'rmXGPMVQnrKAB'



def test_redirector(redismock):
    redismock.set('foo', 'https://example.com')
    with Given(
        app,
        title='Redirect a short url',
        url='/foo'
    ):
        assert status == 302
        assert response.headers['LOCATION'] == 'https://example.com'

        when(title='URL does not exist', url='/notexists')
        assert status == 404
