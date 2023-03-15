# SuperFastPython.com
# example of an asyncio mutual exclusion (mutex) lock
import logging
from random import random, randint
import asyncio

from aioredlock import Aioredlock

redis_instances = [
    "redis://default:redispw@localhost:32768",
]


# task coroutine with a critical section
async def task(lock, num, value):
    # acquire the lock to protect the critical section

    async with await lock_manager.lock("resource") as lock:
        assert lock.valid is True
        assert await lock_manager.is_locked("resource") is True
        # Do your stuff having the lock
        await asyncio.sleep(lock_manager.internal_lock_timeout * 2)
        # lock manager will extend the lock automatically
        assert await lock_manager.is_locked(lock)
        # or you can extend your lock's lifetime manually
        await lock.extend()

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
logging.basicConfig(level=logging.DEBUG)
asyncio.run(main())
