import os
import queue
import socket

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

import select
import threading

def consumer(queues):
    while True:
        can_read, _, _ = select.select(queues, [], [], 0)
        print(can_read)
        for r in can_read:
            item = r.get()
            print('Got:', item)


q1 = PollableQueue()
q2 = PollableQueue()
q3 = PollableQueue()
t = threading.Thread(target=consumer, args=([q1, q2, q3, ], ))
t.daemon = True
t.start()

q1.put(1)
q2.put(10)
q3.put('hello')
q2.put(15)
print("hello fuck")
