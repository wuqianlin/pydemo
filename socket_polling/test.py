import queue
import socket
import asyncio

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

def do_something():
    _collector_trigger.get()
    print("采集数据")


async def trigger():
    while True:
        _collector_trigger.put('触发')
        await asyncio.sleep(2)

loop = asyncio.get_event_loop()
loop.create_task(trigger())
loop.add_reader(_collector_trigger, do_something)
loop.run_forever()
