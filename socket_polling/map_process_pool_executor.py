import time
from concurrent.futures import ThreadPoolExecutor


def get_thread_time(times):
    time.sleep(times)
    return times


start = time.time()
executor = ThreadPoolExecutor(max_workers=4)


def hello_01():
    return 'hello_01'


def hello_02():
    return 'hello_03'

def execute(m):
    return m()

i = 1
for result in executor.map(execute, [hello_01, hello_02]):
    print("task{}:{}".format(i, result))
    i += 1