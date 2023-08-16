#!/usr/bin/env python3

""" This script about creating a class and writing strings to redis."""

import redis
import uuid
from typing import Union


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
