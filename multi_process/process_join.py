"""
主线程等待子线程结束
为了让守护线程执行结束之后，主线程再结束，我们可以使用join方法，让主线程等待子线程执行。
https://docs.python.org/3/library/threading.html
"""
import threading
import time


def run(n):
    print("task", n)
    time.sleep(1)
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')


if __name__ == '__main__':
    # 把子线程设置为守护线程
    t = threading.Thread(target=run, args=("t1",), daemon=True)
    t.start()
    t.join()    # 设置主线程等待子线程结束
    print("end")
