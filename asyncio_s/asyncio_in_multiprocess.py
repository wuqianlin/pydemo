from multiprocessing import Process
import asyncio
import os
import time


async def cost():
    cos = 0
    while True:
        cos += 10
        print(f"I have sleep {cos} second {os.getpid()}")
        # time.sleep(10)
        await asyncio.sleep(10)

async def cost2():
    cos = 0
    while True:
        cos += 10
        print(f"you have sleep {cos} second {os.getpid()}")
        # time.sleep(10)
        await asyncio.sleep(10)


def main():
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(cost())
    finally:
        event_loop.close()


def main2():
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(cost2())
    finally:
        event_loop.close()


ws_client_process = Process(target=main)
ws_client_process.start()

ws_client_process2 = Process(target=main2)
ws_client_process2.start()