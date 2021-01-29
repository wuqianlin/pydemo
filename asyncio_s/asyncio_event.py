"""
事件对象asyncio.Event是基于threading.Event来实现的。事件可以一个信号触发多个协程同步工作，例子如下：
python version: 3.7.3
"""

import time
import asyncio
import functools


def set_event(event):
    print('setting event in callback')
    event.set()


async def coro1(event):
    print('coro1 waiting for event')
    await event.wait()
    print('coro1 triggered')
from concurrent.futures import ThreadPoolExecutor

def get_thread_time(times):
    time.sleep(times)
    return times

# 创建线程池  指定最大容纳数量为4
executor = ThreadPoolExecutor(max_workers=4)
# 通过submit提交执行的函数到线程池中
task1 = executor.submit(get_thread_time, (1))
task2 = executor.submit(get_thread_time, (2))
task3 = executor.submit(get_thread_time, (3))
task4 = executor.submit(get_thread_time, (4))
print("task1:{} ".format(task1.done()))
print("task2:{}".format(task2.done()))
print("task3:{} ".format(task3.done()))
print("task4:{}".format(task4.done()))
time.sleep(2.5)
print('after 2.5s {}'.format('-'*20))

done_map = {
    "task1":task1.done(),
    "task2":task2.done(),
    "task3":task3.done(),
    "task4":task4.done()
}
# 2.5秒之后，线程的执行状态
for task_name,done in done_map.items():
    if done:
        print("{}:completed".format(task_name))


async def coro2(event):
    print('coro2 waiting for event')
    await event.wait()
    print('coro2 triggered')


async def main(loop):
    # Create a shared event
    event = asyncio.Event()
    print('event start state: {}'.format(event.is_set()))

    loop.call_later(5, functools.partial(set_event, event))

    await asyncio.wait([coro1(event), coro2(event)])
    print('event end state: {}'.format(event.is_set()))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
