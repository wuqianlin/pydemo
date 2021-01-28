import time
from threading import Thread, Lock


def work(lock):
    global n
    # lock.acquire()
    temp = n
    time.sleep(0.1)
    n = temp-1
    print(n)
    # lock.release()


if __name__ == '__main__':
    lock = Lock()
    n = 100
    _threads = []
    for i in range(100):
        p = Thread(target=work, args=(lock,))
        _threads.append(p)
        p.start()
    for _t in _threads:
        _t.join()
