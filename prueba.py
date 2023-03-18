import asyncio
import logging
from random import random, randint

import redis.asyncio as redis
from redis import Redis

from redis.exceptions import LockError

connection = Redis(port=32768, password="redispw")
async_connection = redis.Redis(port=32768, password="redispw")

from redis.lock import Lock

import base64
import binascii
import logging
from typing import Any, Optional
from redis.asyncio.lock import Lock
import redis
from redis.lock import Lock


class PimpMyLock(Lock):

    async def __aenter__(self):
        if await self.acquire():
            return self
        raise LockError("Unable to acquire lock within the time specified")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        temp = await self.owned()

        if temp:
            self.release()


import time


async def task(lock, num, value):
    # acquire the lock to protect the critical section
    print(f"task {num}")
    from redis.asyncio.lock import Lock
    # <Handle <TaskStepMethWrapper object at 0x106137eb0>()>

    if connection.lock(name="amlo", sleep=1).locked():

        print(f"sleeping {num}")
    else:
        with connection.lock(name="amlo", blocking=False) as locker:
            if not connection.get("ñema"):
                print(f"Winner acquired {num}")
                await async_connection.set("ñema", f"task {num}")
                return


async def main():
    # create a shared lock
    lock = asyncio.Lock()
    # create many concurrent coroutines
    import random
    coros = [task(lock, (i, e), randint(1, 3)) for i, e in enumerate(random.sample(range(100), k=100))]
    print(coros)
    # execute and wait for tasks to complete

    await asyncio.gather(*coros)
    print(f"\n\nReal winner {connection.get('ñema')}")
    connection.delete("ñema")


logging.basicConfig(level=logging.DEBUG)
asyncio.run(main())
