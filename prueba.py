import asyncio
from random import random

import redis.asyncio as redis

connection = redis.Redis()
from redis.lock import Lock
async def task(lock, num, value):
    # acquire the lock to protect the critical section

    locking_redis = await connection.lock(name="bruh", sleep=1).acquire(blocking=True)
    print(f"LOCKed {num}")
    print(f'>coroutine {num} got the lock, sleeping for {value}')
    # block for a moment
    await asyncio.sleep(value)


    locking_redis = await connection.lock(name="bruh", sleep=1).release()
    print(f"unLOCKed {num}")


# entry point
async def main():
    # create a shared lock
    lock = asyncio.Lock()

    # create many concurrent coroutines
    coros = [task(lock, i, random()) for i in range(10)]
    # execute and wait for tasks to complete

    await asyncio.gather(*coros)

asyncio.run(main())

