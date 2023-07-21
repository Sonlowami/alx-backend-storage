#!/usr/bin/env python3
"""Create a class called Cache"""
import redis
from functools import wraps
from uuid import uuid4
from typing import Union, Callable, Any, List


def count_calls(method: Callable) -> Callable:
    """Count how many functions a method is called"""
    @wraps(method)
    def decorator(self, *args, **kwargs):
        """store the count in redis"""
        name: str = method.__qualname__
        if self._redis.get(name):
            self._redis.set(name, int(self._redis.get(name)) + 1)
        else:
            self._redis.set(name, 1)
        return method(self, *args, **kwargs)
    return decorator


def call_history(method: Callable) -> Callable:
    """decorator to store the input and output of a method"""
    @wraps(method)
    def decorator(self, *args, **kwargs):
        """store input and output history of a method in redis"""
        input_name: str = method.__qualname__ + ":inputs"
        output_name: str = method.__qualname__ + ":outputs"
        self._redis.rpush(input_name, str(args))
        output: Any = method(self, *args, **kwargs)
        self._redis.rpush(output_name, output)
        return output
    return decorator


class Cache:
    """Create a cache class"""

    def __init__(self):
        """create an instance of redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data into redis"""
        new_id = str(uuid4())
        if self._redis.set(new_id, data):
            return new_id

    def get(self, key: str,
            fn: Union[Callable[[bytes], str], None] = None) -> str:
        """Retrieve a key in appropriate type"""
        byte_data: Union[bytes, None] = self._redis.get(key)
        if not byte_data or not fn:
            return byte_data
        return fn(byte_data)

    def get_str(self, byte_data: bytes) -> str:
        """Retrieve a string from a bytes object"""
        return byte_data.decode('utf-8')

    def get_int(self, bytes_data: bytes) -> int:
        """Retrieve an int from a bytes object"""
        return int(bytes_data)


def replay(method: Callable) -> None:
    """Make a replay of history of method calls"""
    _redis = redis.Redis()
    count: int = int(_redis.get(method.__qualname__))
    inputkey: str = method.__qualname__ + ":inputs"
    outkey: str = method.__qualname__ + ":outputs"
    print("{} was called {} times:".format(method.__qualname__, count))
    ins: List = list(_redis.lrange(inputkey, 0, -1))
    outs: List = list(_redis.lrange(outkey, 0, -1))
    history: List = list(zip(ins, outs))
    for pair in history:
        print("{}(*{}) -> {}".format(method.__qualname__,
                                     pair[0].decode('utf-8'),
                                     pair[1].decode('utf-8')))
