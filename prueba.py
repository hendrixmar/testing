import asyncio
import logging
from random import random

import redis.asyncio as redis

connection = redis.Redis(port=32768, password="redispw")
from redis.lock import Lock

import base64
import binascii
import logging
from typing import Any, Optional

import redis
from redis.lock import Lock




class Redis:

    def __init__(
            self,
            host_name: str,
            port_number: int,
            username: str,
            password: str,
            ssl: bool,
            ssl_cert_reqs: Optional[str],
            logger: logging.Logger,
            socket_timeout: Optional[int] = None,
            socket_connect_timeout: Optional[int] = None,
            health_check_interval: int = 0
    ) -> None:
        self.__logger: logging.Logger = logger
        self.__redis: redis.Redis = redis.Redis(
            host=host_name,
            port=port_number,
            username=username,
            password=password,
            ssl=ssl,
            ssl_cert_reqs=ssl_cert_reqs,
            socket_timeout=socket_timeout,
            socket_connect_timeout=socket_connect_timeout,
            health_check_interval=health_check_interval
        )
    def __call__(self,
                         lock_key: str,
                         timeout: Optional[int] = None,
                         sleep: float = 0.1,
                         blocking: bool = True,
                         blocking_timeout_in_seconds: Optional[int] = None):
        self.lock_instance = self.__redis.lock(
                name=lock_key,
                timeout=timeout,
                sleep=sleep,
                blocking=blocking,
                blocking_timeout=blocking_timeout_in_seconds
            )
        return self
    async def __aenter__(self):
        try:
            self.lock_instance.acquire()
        except redis.exceptions.RedisError:
            self.__logger.exception('Redis error while acquiring the lock')
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


async def task(lock, num, value):
    # acquire the lock to protect the critical section
    print("bruh")
    from redis.asyncio.lock import Lock

    async with connection.lock(name="amlo", sleep=0.3):
        print(f"acquired {num}")


async def main():
    # create a shared lock
    lock = asyncio.Lock()
    # create many concurrent coroutines
    coros = [task(lock, i, random()) for i in range(10)]
    # execute and wait for tasks to complete

    await asyncio.gather(*coros)


logging.basicConfig(level=logging.DEBUG)
asyncio.run(main())
