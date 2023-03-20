import abc
import asyncio
import time
import random
from pprint import pprint

from random import randint
from typing import Any, Union, Optional, Dict, Callable

import redis.asyncio as redis
from redis import Redis

from redis.exceptions import LockError
import sys

import logging

from redis.lock import Lock

connection = Redis()
async_connection = redis.Redis()


class ReadWriteLockInterface(abc.ABC):

    @abc.abstractmethod
    def distributed_read(self, key: str, key_lock: Optional[str]) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def distributed_write(self, key: str,
                          old_value: Dict[str, Any],
                          callable_process: Callable[[Any], Dict],
                          key_lock: Optional[str] = None) -> bool:
        raise NotImplementedError


class RedisRepository(ReadWriteLockInterface):

    def __init__(self):
        self.__redis_async_connection = redis.Redis()
        self.__redis_connection = Redis()
        self.__sleep_time = 0.000001

    async def distributed_write(self,
                                key: str,
                                old_value: Dict[str, Any],
                                callable_resource: Callable[[Any], Dict],
                                key_lock: Optional[str] = None) -> Optional[Dict]:
        key_lock = key_lock or f"{key}_lock"

        def decoder(elements: Dict[str, Any]) -> Dict[str, Any]:
            temp = {}
            for k, v in elements.items():
                if isinstance(k, bytes):
                    k = k.decode()
                if isinstance(v, bytes):
                    v = v.decode()
                temp.update({k: v})

            return temp

        with self.__redis_connection.lock(name=key_lock):

            if decoder(self.__redis_connection.hgetall(key)) == old_value:
                value = callable_resource()
                self.__redis_connection.hset(name=key,
                                             mapping={"name": value})
                return {"name": value}

        return None

    async def distributed_read(self,
                               key: str,
                               key_lock: Optional[str] = None) -> Any:

        key_lock = key_lock or f"{key}_lock"
        while self.__redis_connection.lock(name=key_lock).locked():
            await asyncio.sleep(0.0001)

        return await self.__redis_async_connection.hgetall(key)


import time

# hset uniteller name 'el pepe'
import itertools


async def task(num, value):
    # acquire the lock to protect the critical section
    print(f"task {num}")
    from redis.asyncio.lock import Lock
    # <Handle <TaskStepMethWrapper object at 0x106137eb0>()>

    if fetched_data := await lol.distributed_read("uniteller"):
        return fetched_data

    if result := await lol.distributed_write("uniteller", {}, lambda: value):
        print(f"Winner acquired {value}")
        return result

    return await lol.distributed_read("uniteller")


async def main():
    # create a shared lock

    # create many concurrent coroutines
    import random
    n = 1000
    coros = [task(i, i) for i in range(n)]

    # execute and wait for tasks to complete

    bruh = await asyncio.gather(*coros)


if __name__ == "__main__":
    lol = RedisRepository()
    from time import perf_counter


    # Start the stopwatch / counter
    t1_start = perf_counter()

    asyncio.run(main())
    # Stop the stopwatch / counter
    t1_stop = perf_counter()
    print(f"\n\nReal winner {connection.hgetall('uniteller')}")
    print("Elapsed time:", t1_stop, t1_start)

    print("Elapsed time during the whole program in seconds:",
          t1_stop - t1_start)
    # time.sleep(randint(15,20))

    logging.basicConfig(level=logging.DEBUG)

    print(connection.hgetall("SACA"))
    connection.delete("uniteller")
