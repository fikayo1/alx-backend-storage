#!/usr/bin/env python3
"""
Redis implementation with redis-py
"""
import redis
import uuid
from typing import Union
from typing import Callable

class Cache():
    """ A redis client instance"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()


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
        
