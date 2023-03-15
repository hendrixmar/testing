from aioredlock import Aioredlock, LockError, Sentinel
import asyncio

# Define a list of connections to your Redis instances:
redis_instances = [

  'redis://default:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81@localhost:6379',

]

async def main():
    # Create a lock manager:
    lock_manager = Aioredlock(redis_instances)

    # Check wether a resourece acquired by any other redlock instance:
    assert not await lock_manager.is_locked("resource_name")

    # Try to acquire the lock:
    try:
        lock = await lock_manager.lock("resource_name", lock_timeout=10)
    except LockError:
        print('Lock not acquired')
        raise

    #lock2 = await lock_manager.lock("resource_name", lock_timeout=10)

    # Now the lock is acquired:
    assert lock.valid
    lol = await lock_manager.is_locked("resource_name")
    print(lol)
    # Extend lifetime of the lock:
    await lock_manager.extend(lock, lock_timeout=10)
    # Raises LockError if the lock manager can not extend the lock lifetime
    # on more then half of the Redis instances.

    # Release the lock:
    await lock_manager.unlock(lock)
    # Raises LockError if the lock manager can not release the lock
    # on more then half of redis instances.

    # The released lock become invalid:
    assert not lock.valid
    assert not await lock_manager.is_locked("resource_name")

    # Or you can use the lock as async context manager:
    try:
        async with await lock_manager.lock("resource_name") as lock:
            assert lock.valid is True
            # Do your stuff having the lock
            await lock.extend()  # alias for lock_manager.extend(lock)
            # Do more stuff having the lock
        assert lock.valid is False # lock will be released by context manager
    except LockError:
        print('Lock not acquired')
        raise

    # Clear the connections with Redis:
    await lock_manager.destroy()


if __name__ == "__main__":

    asyncio.run(main())
    asyncio.run(main())
    asyncio.run(main())
