#!/usr/bin/env python3

""" This script about creating a class and writing strings to redis."""

import redis
import uuid
from typing import Union, Callable
from functools import wraps



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

    def count_calls(method: Callable) -> Callable:
        """ Above Cache define a count_calls decorator that takes a single method
            Callable argument and returns a Callable.
        """

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper
    
    def call_history(method: Callable) -> Callable:
        """ this task, we will define a call_history decorator to store the history of
            inputs and outputs for a particular function.
        """
    
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            input_key = f"{method.__qualname__}:inputs"
            output_key = f"{method.__qualname__}:outputs"
            
            self._redis.rpush(input_key, str(args))
            
            output = method(self, *args, **kwargs)
            self._redis.rpush(output_key, str(output))
            
            return output
        return wrapper
    
    def replay(fn):
        """
        Display the history of calls of a particular function.
        """
        # Get the qualified name of the function
        fn_name = fn.__qualname__
        
        # Get the keys for input and output history
        input_key = f"{fn_name}:inputs"
        output_key = f"{fn_name}:outputs"
        
        # Retrieve the list of inputs and outputs from Redis
        inputs = cache._redis.lrange(input_key, 0, -1)
        outputs = cache._redis.lrange(output_key, 0, -1)
        
        # Print the history of calls
        print(f"{fn_name} was called {len(inputs)} times:")
        for i, (input_data, output_data) in enumerate(zip(inputs, outputs)):
            input_args = eval(input_data)  # Convert the string back to args tuple
            output_key = output_data.decode("utf-8")  # Decode the byte string
            print(f"{fn_name}(*{input_args}) -> {output_key}")