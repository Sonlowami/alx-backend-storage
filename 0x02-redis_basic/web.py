#!/usr/bin/env python3
"""Make a query to a url and return the html"""
import requests
import redis


def get_page(url: str) -> str:
    """Get a page and return it's content"""
    _redis = redis.Redis()
    page: str = requests.get(url)
    key: str = 'count:{}'.format(url)
    _redis.incr(key)
    return page
