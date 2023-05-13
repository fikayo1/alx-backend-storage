#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker."""
import redis
import requests


def get_page(url: str) -> str:
    """Make a get request to a url and caches the result."""
    cache = redis.Redis()
    cache.incr("count:" + url)
    resp = cache.get("result:" + url)
    if resp is None:
        resp = requests.get(url).text
        cache.setex("result:" + url, 10, resp)
    else:
        resp.decode("utf-8")
    return resp
