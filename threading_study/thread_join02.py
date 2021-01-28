"""
2. 设置守护线程
注意请确保setDaemon()在start()之前。
非常明显的看到，主线程结束以后，子线程还没有来得及执行，整个程序就退出了。
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
        t.setDaemon(True)
        t.start()

    print('主线程结束了！', threading.current_thread().name)
    print('一共用时：', time.time()-start_time)
