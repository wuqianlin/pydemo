"""
Value、Array是通过共享内存的方式共享数据
Manager是通过共享进程的方式共享数据。

进程之间共享数据(数值型 - Value)：
"""
import multiprocessing


def func(d):
    d.value = 10.78  # 子进程改变数值的值，主进程跟着改变


if __name__ == "__main__":
    _d = multiprocessing.Value("d", 10.0)  # d表示数值,主进程与子进程共享这个value。（主进程与子进程都是用的同一个value）
    print(_d.value)

    p = multiprocessing.Process(target=func, args=(_d,))
    p.start()
    p.join()

    print(_d.value)
