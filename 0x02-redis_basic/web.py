#!/usr/bin/env python3
"""Make a query to a url and return the html"""
import requests
import redis


def get_page(url: str) -> str:
    """Get a page and return it's content"""
    _redis = redis.Redis()
    countkey: str = 'count:{}'.format(url)
    contentkey: str = '{}'.format(url)
    page: str = requests.get(url)
    _redis.set(contentkey, page)
    _redis.expire(contentkey, 10)
    _redis.incr(countkey)
    return page
