"""
Value、Array是通过共享内存的方式共享数据
Manager是通过共享进程的方式共享数据。

进程之间共享数据(数组型 - Array)：
"""

import multiprocessing


def func(i):
    i[2] = 9999  # 子进程改变数组，主进程跟着改变


if __name__ == "__main__":
    _i = multiprocessing.Array("i", [1, 2, 3, 4, 5])  # 主进程与子进程共享这个数组
    print(_i[:])

    p = multiprocessing.Process(target=func, args=(_i,))
    p.start()
    p.join()

    print(_i[:])
