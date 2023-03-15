# SuperFastPython.com
# example of an asyncio mutual exclusion (mutex) lock
from random import random, randint
import asyncio

from aioredlock import Aioredlock


redis_instances = [
    'redis://redis:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81@0.0.0.0:6379',
]


# task coroutine with a critical section
async def task(lock, num, value):
    # acquire the lock to protect the critical section

    while await lock_manager.is_locked("resource_name"):
        async with lock:
            print(f'>coroutine {num} got the lock, sleeping for {value}')
            # block for a moment
            await asyncio.sleep(value)
        print(f"LOCKed {num}")

    print(f"unLOCKed {num}")


# entry point
async def main():
    # create a shared lock
    lock = asyncio.Lock()
    # create many concurrent coroutines
    coros = [task(lock, i, random()) for i in range(10)]
    # execute and wait for tasks to complete
    lock = await lock_manager.lock("resource_name", lock_timeout=0.1)
    await asyncio.gather(*coros)



lock_manager = Aioredlock(redis_instances)
# run the asyncio program

asyncio.run(main())


