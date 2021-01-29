import asyncio
import queue
from socket import socketpair
from threading import Thread


class PollableQueue(queue.Queue):
    def __init__(self):
        super().__init__()
        self._putsocket, self._getsocket = socketpair()

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

async def collect_interval(interval: int):
    while True:
        _collector_trigger.put('fuck the world')
        await asyncio.sleep(interval)


def advance_start_device_info_collector():
    data = _collector_trigger.get()
    print(data)
    _device_info_collector_queue.put({'data': 'nothing'})


def advance_report_device_info():
    data = _device_info_collector_queue.get()
    print(data)
    new_loop = asyncio.new_event_loop()
    t = Thread(target=start_loop, args=(new_loop,))
    t.start()


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ss())
    loop.run_forever()


async def ss():
    await asyncio.sleep(2)
    print("ws.send data")


loop = asyncio.get_event_loop()
loop.add_reader(_collector_trigger, advance_start_device_info_collector)
loop.add_reader(_device_info_collector_queue, advance_report_device_info)
loop.create_task(collect_interval(2))


try:
    loop.run_forever()
finally:
    loop.close()

