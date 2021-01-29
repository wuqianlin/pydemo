import asyncio
import queue
import socket
import select
from threading import Thread


class PollableQueue(queue.Queue):
    def __init__(self):
        super().__init__()
        self._putsocket, self._getsocket = socket.socketpair()

    def fileno(self):
        return self._getsocket.fileno()

    def put(self, item):
        super().put(item)
        self._putsocket.send(b'x')

    def get(self):
        self._getsocket.recv(1)
        return super().get()


_collector_trigger = PollableQueue()
_device_info_collector_queue = PollableQueue()


async def start_server():
    asyncio.create_task(collect_interval(2))
    asyncio.create_task(async_advance_start_device_info_collector())
    asyncio.create_task(advance_report_device_info())


async def collect_interval(interval: int):
    while True:
        _collector_trigger.put('collect trigger')
        await asyncio.sleep(interval)


async def async_advance_start_device_info_collector():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, async_advance_report_device_info)


def advance_start_device_info_collector():
    while True:
        can_read, _, _ = select.select([_collector_trigger], [], [])
        for r in can_read:
            if r == _collector_trigger:
                print(r.get())
                _device_info_collector_queue.put({'data': 'nothing'})


async def async_advance_report_device_info():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, advance_report_device_info)

def advance_report_device_info():
    new_loop = asyncio.new_event_loop()
    while True:
        can_read, _, _ = select.select([_device_info_collector_queue], [], [])
        for r in can_read:
            t = Thread(target=start_loop, args=(new_loop,))
            t.start()

            # device_info = r.get()
            # print(device_info)


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ss())
    loop.run_forever()


async def ss():
    await asyncio.sleep(2)
    print("hellfuck")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_server())

    try:
        loop.run_forever()
    finally:
        loop.close()