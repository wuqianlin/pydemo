"""
守护线程:
这里使用setDaemon(True)把子线程变成了主线程的守护线程，
当主线程结束时，子线程也将立即结束，不再执行。
https://docs.python.org/3/library/threading.html
"""
import threading
import time


def run(n):
    print("task", n)
    time.sleep(1)
    print('1')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('3')


if __name__ == '__main__':
    t = threading.Thread(target=run, args=("t1",))
    t.setDaemon(True)   # 把子进程设置为守护线程，必须在start()之前设置
    t.start()
    print("end")
