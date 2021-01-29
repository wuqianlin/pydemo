import asyncio

async def doAsync():
    await asyncio.sleep(0)


def runEventLoop(loop):
    # loop = asyncio.new_event_loop()
    print('event', id(loop))
    asyncio.set_event_loop(loop)
    loop.run_until_complete(doAsync())
    loop.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    runEventLoop(loop)
    runEventLoop(loop)