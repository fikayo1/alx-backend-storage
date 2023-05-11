#!/usr/bin/env python3
"""
Redis implementation with redis-py
"""
import redis
import uuid
from typing import Union

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
