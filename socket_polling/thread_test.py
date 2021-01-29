import asyncio
from threading import Thread


async def hello():
    await asyncio.sleep(2)
    print("hello")

t = Thread(target=hello)
t.start()
