# -*- coding: utf-8 -*-


import asyncio


async def a():
    print('Suspending a')
    await asyncio.sleep(2)
    print('Resuming a')
    return 'A'


async def b():
    print('Suspending b')
    await asyncio.sleep(1)
    print('Resuming b')
    return 'B'


async def c1():
    task1 = asyncio.shield(a())
    task2 = asyncio.create_task(b())
    task1.cancel()
    result = await asyncio.gather(task1, task2, return_exceptions=True)
    print(result)


async def c2():
    task1 = asyncio.shield(b())
    task2 = asyncio.create_task(a())
    task1.cancel()
    result = await asyncio.gather(task1, task2, return_exceptions=True)
    print(result)


async def c3():
    task1 = asyncio.shield(a())
    task2 = asyncio.create_task(b())
    ts = asyncio.gather(task1, task2, return_exceptions=True)
    task1.cancel()
    result = await ts
    print(result)


if __name__ == '__main__':
    # asyncio.run(c1())
    loop = asyncio.get_event_loop()
    # loop.create_task(c1())
    # loop.create_task(c2())
    # loop.create_task(c3())
    loop.run_forever()


"""
result c1:
Suspending a
Suspending b
Resuming b
[CancelledError(), 'B']
Resuming a

result c2:
Suspending b
Suspending a
Resuming b
Resuming a
[CancelledError(), 'A']

result c3:
Suspending a
Suspending b
Resuming b
[CancelledError(), 'B']
Resuming a

可以看出task1 = asyncio.shield(a()) 中shield保护了task1中的a()的完整执行，与官网上
所说的一致，即保护a()不被取消
"""
