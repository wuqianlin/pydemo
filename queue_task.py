"""
https://docs.python.org/zh-cn/3.6/library/queue.html
慢速生产-快速消费
快速生产-慢速消费
"""
import time
import queue
import threading

num_worker_threads = 3
q = queue.Queue()
threads = []


def do_work(data):
    time.sleep(0.5)
    print(f'do work: {data}')


def source():
    return range(1, 10)


def worker():
    while True:
        _item = q.get()
        if _item is None:
            break
        do_work(_item)
        q.task_done()


for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in source():
    time.sleep(1)
    q.put(item)

# block until all tasks are done
print('queue.join before!')
q.join()
print('queue.join after!')

# stop workers
for i in range(num_worker_threads):
    q.put(None)
    print("put None")
for t in threads:
    t.join()


