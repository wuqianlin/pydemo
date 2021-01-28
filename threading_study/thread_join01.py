"""
1. Python多线程的默认情况
我们的计时是对主线程计时，主线程结束，计时随之结束，打印出主线程的用时。
主线程的任务完成之后，主线程随之结束，子线程继续执行自己的任务，直到全部的子线程的任务全部结束，程序结束。
"""
import threading
import time


def run():
    time.sleep(2)
    print('当前线程的名字是： ', threading.current_thread().name)
    time.sleep(2)


if __name__ == '__main__':
    start_time = time.time()
    print('这是主线程：', threading.current_thread().name)
    thread_list = []
    for i in range(5):
        t = threading.Thread(target=run)
        thread_list.append(t)

    for t in thread_list:
        t.start()

    print('主线程结束！', threading.current_thread().name)
    print('一共用时：', time.time()-start_time)
