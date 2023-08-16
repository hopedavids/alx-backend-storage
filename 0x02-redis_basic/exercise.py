#!/usr/bin/env python3

""" This script about creating a class and writing strings to redis."""

import redis
import uuid
from typing import Union, Callable


class Cache:
    """ Create a Cache class. In the __init__ method, store an instance
       of the Redis client as a private variable named _redis
       (using redis.Redis()) and flush the instance using flushdb.
    """

    def __init__(self):
        self._redis = redis.Redis(host='localhost', port=6379)
        self._redis.flushdb()

    def store(self, data: Union[str, float, int, bytes]) -> str:
        """ Create a store method that takes a data argument and returns
            a string. The method should generate a random key
            (e.g. using uuid),store the input data in Redis using the
            random key and return the key.
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, float, int, bytes]:
        """ In this method we will create a get method that take a key string
            argument and an optional Callable argument named fn. This callable
            will be used to convert the data back to the desired format.
        """

        cached_data = self._redis.get(key)
        if cached_data:
            if fn:
                return fn(cached_data)
            return cached_data
        return None

    def get_str(self, key: str) -> Union[str, bytes, None]:
        """ This method return a decoded key string format to a more readable
            format.
        """

        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, bytes, None]:
        """ This method returns a decoded key integer format. """

        return self.get(key, fn=int)
