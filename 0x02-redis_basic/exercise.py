#!/usr/bin/env python3
"""
Redis implementation with redis-py
"""
import redis
import uuid
from typing import Union
from typing import Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """Decorate a function to keep its call history."""
    @wraps(method)
    def new_method(self, *args):
        """Do the same thing as previous method but also record history."""
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        res = method(self, *args)
        self._redis.rpush(method.__qualname__ + ":outputs", res)
        return res
    return new_method


def count_calls(method: Callable) -> Callable:
    """A decorator for counting calls"""
    @wraps(method)
    def new_method(self, *args, **kwds):
        """A method that does all previous plus count calls"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwds)
    return new_method


    key = method.__qualname__
class Cache():
    """ A redis client instance"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()


    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """A method to store data in redis"""
        key = uuid.uuid4()
        self._redis.set(str(key), data)
        return str(key)

    def get(self, key: str, fn: Union[Callable, None] = None) -> Union[int, float, str, bytes, None]:
        """A method to retrieve data from redis"""
        if fn is None:
            return self._redis.get(key)
        return fn(self._redis.get(key))


    def get_int(self, key: str) -> int:
        """Get an integer from the cache."""
        return int(self._redis.get(key))

    def get_str(self, key: str) -> str:
        """Get a string from the cache."""
        data = self._redis.get(key)
        return data.decode("utf-8")
        
